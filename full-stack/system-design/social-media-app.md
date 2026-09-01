# Social Media App — Design Document

Design a simple social media application: an X/Twitter-like service with an
asymmetric follow graph, short text posts with images and video, a home feed,
engagement features (likes, comments, reposts), private accounts and blocking.
Assumed scale: ~10M DAU. Canonical interview components to cover: ranking,
databases, privacy controls, engagement, hosting of user-generated content,
and the database schema.

> **Core insight — this is a feed-delivery app with posting attached, not a
> posting app with a feed feature.** The write path (~230 posts/s) is trivial;
> the read path is the system. Every architectural decision below exists to
> serve ~2B feed deliveries a day under 300 ms without letting any single
> write amplify out of control.

## 1. Requirements & Scale

**Functional**

- Post short text (≤ 280 chars) with optional images or video
- Follow / unfollow — asymmetric, no approval for public accounts
- Home feed: posts from people you follow, newest-first
- Like, comment, repost
- Private accounts (follow requests require approval); block users

**Non-functional**

- **Feed p95 < 300 ms** — a slow feed is a dead product; this is the binding
  latency constraint
- **Uploads async** — posting never waits on media processing
- **Read-heavy** — stated up front because it shapes every section below
- Engagement counts may be eventually consistent (display-only)
- Highly available; bias failures toward available-and-stale

**Back-of-envelope scale**

| Metric | Assumption | Number |
|---|---|---|
| Posts | 2 per DAU/day | 20M/day ≈ 230/s avg, ~2.5K/s peak |
| Likes + comments | 5 per DAU/day | 50M/day |
| Total writes | posts + engagement | ~70M/day (~800/s avg) |
| Feed refreshes | 10 per DAU/day | 100M/day ≈ 1.2K/s avg, ~12K/s peak |
| Total reads | feed + profiles + hydration + notifications | ~1B/day ≈ 12K/s avg, ~50K/s peak |

The shaping number is **fan-out amplification**: the average user has ~200
followers, so each of the 20M daily posts lands in ~100–200 feeds — **~2B post
deliveries/day. Every post is written once but delivered ~100 times.**
Write:read ≈ 1:100.

## 2. High-Level Architecture

```
                    media GETs (~300 TB/day)
   Clients ────────────────────────────────────────> CDN
     │                                                │ miss
     │                                                v
     │  presigned PUT (direct)              Object store (S3)
     │ ─────────────────────────────────────────────> raw/ + variants
     │ HTTPS
     v
     LB ──> API services (feed / post / social / media)
              │                 │                │
              │ feed reads      │ writes         │ events (post_created,
              │ (hot path)      │ (truth, once)  │  media_ready, liked)
              v                 v                v
           Redis            Postgres          Kafka ──> Workers
      feed:{user}         (source of          fan-out / resize /
      celeb_posts:{id}     truth)             notifications
      counters                  ^                  │
                                 └──── writeback ───┘
                     (variants ready, counter flush, notifications)
```

Three consequences of this shape:

1. **Media never crosses the API tier.** Clients upload to object storage
   directly via pre-signed URLs (§5); reads hit the CDN (§6). API servers move
   metadata only.
2. **Postgres is written once per action.** The 100× read amplification
   happens after the synchronous path, in workers — the synchronous path stays
   O(1) and all multiplied work is queued.
3. **Redis holds precomputed feeds** — the materialized result of fan-out. It
   is a cache of Postgres data, rebuildable, which makes its loss a
   degradation rather than an outage (§10).

## 3. Data Model

Postgres, not NoSQL, and the why matters: the core data is small and deeply
relational (users ↔ follows ↔ posts); write volume (~800/s avg) is far below
Postgres's comfort zone; and the hot read path does not touch Postgres at all
once §4's cache is in place. Reaching for Cassandra here pays sharding costs
before having a sharding problem (§10).

```sql
create table users (
    id             bigint primary key,
    username       varchar(30) not null unique,
    display_name   varchar(80) not null,
    bio            varchar(200),
    avatar_key     text,
    is_private     boolean not null default false,
    follower_count bigint not null default 0,
    following_count bigint not null default 0,
    post_count     bigint not null default 0,
    created_at     timestamptz not null default now(),
);

create table follows (
    follower_id bigint not null references users(id),
    followee_id bigint not null references users(id),
    status      varchar(10) not null default 'accepted',
    created_at  timestamptz not null default now(),
    primary key (follower_id, followee_id),
);
create index follows_followee_idx
    on follows (followee_id) where status = 'accepted';

create table posts (
    id            bigint primary key,
    author_id     bigint not null references users(id),
    body          varchar(280),
    media_id      bigint,
    like_count    bigint not null default 0,
    comment_count bigint not null default 0,
    repost_count  bigint not null default 0,
    created_at    timestamptz not null default now(),
);
create index posts_author_time_idx on posts (author_id, created_at desc);

create table media (
    id          bigint primary key,
    owner_id    bigint not null references users(id),
    storage_key text not null,
    mime_type   text not null,
    status      varchar(10) not null default 'pending',
    variants    jsonb,
    created_at  timestamptz not null default now(),
);

create table likes (
    user_id    bigint not null references users(id),
    post_id    bigint not null references posts(id),
    created_at timestamptz not null default now(),
    primary key (user_id, post_id),
);
create index likes_post_idx on likes (post_id);

create table comments (
    id         bigint primary key,
    post_id    bigint not null references posts(id),
    author_id  bigint not null references users(id),
    body       varchar(1000) not null,
    created_at timestamptz not null default now(),
);
create index comments_post_idx on comments (post_id, created_at desc);

create table blocks (
    blocker_id bigint not null references users(id),
    blocked_id bigint not null references users(id),
    created_at timestamptz not null default now(),
    primary key (blocker_id, blocked_id),
);
```

Modeling decisions:

- **Snowflake post IDs** — `id` encodes timestamp, so `ORDER BY id DESC` is
  chronological and feed merges (§4) compare IDs without touching
  `created_at`. Free sorting where it matters.
- **Counters denormalized** onto `posts`/`users` and maintained out-of-band
  (§7). Never `count(*)` on a read path.
- **`follows.status`** — private accounts are the same table with `'pending'`
  rows: one graph, two states, no second schema (§8).
- **`posts` partitioned** by `created_at` (monthly ranges), not sharded —
  ~20M posts/day at ~1 KB is a few TB/year, comfortable on one Postgres with
  replicas for years. Partitioning buys cheap archiving and small indexes.

## 4. Feed Generation — Hybrid Fan-Out

How 12K feed requests/s (peak) get served in 300 ms. The design is taught as
a progression; each step's failure motivates the next.

**Attempt 1 — pull on read** (compute the feed when asked):

```sql
select p.* from posts p
join follows f on p.author_id = f.followee_id
where f.follower_id = :me and f.status = 'accepted'
order by p.created_at desc limit 20;
```

Correct, and fine at 100K users. It dies at 10M DAU: following ~400 people
means Postgres merges 400 sorted per-author index lists per request. At 12K
requests/s peak that is a multi-hundred-row merge against a cache-cold
working set — CPU-bound collapse. No index fixes it, because the merge width
*is* the follow count.

**Attempt 2 — push on write** (precompute the feed). On `post_created`,
fan-out workers load the author's followers and append the post ID to each
follower's feed:

```
feed:{user_id}  →  Redis list of post IDs, capped at ~400 entries
```

- Read becomes `LRANGE feed:{me} 0 19` plus one batched hydration of 20 rows
  — O(requested), not O(list); the list *is* the SELECT … JOIN … ORDER BY …
  LIMIT, materialized in advance.
- `LRANGE key start stop` returns an inclusive index slice of a Redis list.
  Fan-out always `LPUSH`es at the head, so the list stays newest-first for
  free, and `LTRIM feed:{me} 0 399` caps its length.
- Write amplification is the cost: an average post → ~200 pushes (fine). A
  **celebrity post → 10M pushes** — one post from a 10M-follower account
  occupies the entire fan-out cluster for minutes; a live event backs the
  queue up behind it and everyone else's posts lag. This is the celebrity
  problem.
- Storage is never the blocker: 10M feeds × 400 IDs × 8 B ≈ 40–80 GB — a
  small Redis cluster.

**Concluded design — hybrid.** Authors above ~100K followers are flagged
celebrities (power law: only a few thousand accounts qualify).

| Author type | On post write | On feed read |
|---|---|---|
| Normal (< 100K followers) | push to followers' Redis feeds | `LRANGE` only — O(1) |
| Celebrity (≥ 100K) | **no push**; the post just lands in Postgres | pull the celebrity's recent posts and merge |

A celebrity's post is **not delivered to Redis by anyone**. Delivery happens
inside followers' feed requests:

```
feed request for user 42:
  1. LRANGE feed:42 0 19            ← normal users' posts (pushed earlier)
  2. read celeb_posts:{author_id}    ← or SELECT ... WHERE author_id IN (…)
     for each celebrity followed       via posts_author_time_idx, live
  3. merge + dedupe by post_id + sort → fill the page → hydrate → serve
```

Step 2 is a handful of index hits per request (users follow at most a few
celebrities), so the pull cost is noise against a read path that runs anyway.
One celebrity post then costs 1 Postgres insert instead of 10M pushes:

| | Push (fan-out) | Pull (hybrid) |
|---|---|---|
| Write time | 10M LPUSHes — minutes of cluster capacity for one post | 1 Postgres insert |
| Read time | O(1) LRANGE | + a few indexed lookups per feed view |
| Total | a massive write spike that crowds out everyone's fan-out | ~10M cheap reads, spread across refreshes that were happening anyway |

Refinement: cache the celebrity's recent posts **once** —
`celeb_posts:{author_id}` → last ~50 post IDs, updated when they post (one
write per celebrity post) — and merge from that. The deep pattern: **cache
the author's timeline once and share it across all followers, instead of
copying it into each of the 10M followers' feeds.** One shared copy beats 10M
per-user copies when the content is identical.

## 5. Media Upload Pipeline & Consistency

Two stores — a Postgres row and an S3 object — with no cross-store
transaction possible (S3 has no prepare/commit). The guarantee comes from a
persisted state machine whose every crash-state is recoverable, plus a
reconciler. **`media.status` is the transaction** — the entire lifecycle's
truth lives in one Postgres column, where real transactions exist.

```
                    Postgres (transactional truth)
   ┌──────────┐   ┌──────────┐   ┌────────┐   ┌─────────────┐
   │ (none)   │-->│ pending  │-->│ ready  │-->│ referenced  │
   └──────────┘   └──────────┘   └────────┘   │ by a post   │
                     ^              ^         └─────────────┘
        API inserts  │   resize     │  worker: variants written,
        row BEFORE   │   worker     │  UPDATE status = 'ready'
        any upload   │              │
                     v              v
                    S3          S3 raw/ + variant keys
                 (nothing)     (immutable, content-keyed)
```

**Ordering invariants** — each closes a specific hole:

- **a) The media row (`pending`) exists before any bytes move.** The API
  creates it when handing out the pre-signed URL, so an abandoned upload is
  always a findable row, never untracked S3 garbage.
- **b) A post row can only be created when its media is `ready`** (video
  relaxation below) — no feed can ever render broken media.
- **c) Only a GC that proves no post references a media object may delete
  it.** Nothing else deletes S3 objects, so referenced media cannot vanish
  under a live post.

**The one true transaction — single-store.** "Insert this post iff its media
is mine and ready" as one atomic statement, so there is no check-then-insert
race and no cross-user media mounting:

```sql
insert into posts (id, author_id, body, media_id, created_at)
select :id, :me, :body, m.id, now()
from media m
where m.id = :media_id
  and m.owner_id = :me
  and m.status = 'ready';
-- zero rows inserted → reject the request
```

**Crash points, enumerated** — the honest version of "guaranteed":

| Crash point | Leftover state | Recovery |
|---|---|---|
| Client never uploads / abandons | `pending` row, no bytes | Reaper: `pending` > 24h → delete row; S3 lifecycle rule aborts incomplete multipart uploads |
| Upload lands, worker crashes pre-variants | `pending` row + `raw/` object | Reconciler re-enqueues; the raw object existing means the work is recoverable |
| Worker writes variants, dies pre-UPDATE | variants on disk, still `pending` | Retry re-runs transcode; keys are deterministic (`media_id` + size), so it overwrites itself — idempotent |
| Worker sets `ready`, user never posts | `ready`, unreferenced | GC: ready + unreferenced after N days → delete objects, then row |
| Post insert commits | post references ready media | Terminal, safe — invariant (c) protects it |

**Failure bias:** never render broken media. In doubt, hold the post or show
text-plus-placeholder; a visible broken-image icon is the one unrecoverable
outcome because it is user-visible.

**Video relaxation:** images block post creation on `ready` (transcode ~1s),
but video (minutes) posts once a *minimal* rendition exists — first HLS
variant + thumbnail — then gains higher renditions in `variants` as they
land. The feed never shows nothing and never shows a dead player; it shows
progressively better media.

## 6. Media Delivery & CDN Cost Control

Reads: **CDN in front of S3**, immutable content-addressed keys, long TTL —
an unbounded cache hit ratio (the §5 key scheme exists for this). Budget:
~30% of posts carry media → ~6M images/day × ~2 MB with variants ≈ ~12 TB/day
storage and ~300 TB/day CDN egress. The CDN is not an optimization; it is the
tier carrying most of the product's bytes.

Cost = **(deliveries) × (bytes per delivery) × ($ per GB)**, minus what
caching absorbs. Control each term:

- **Bytes per delivery — the biggest lever.** Never serve originals: the feed
  tile gets the 480px variant, the detail view gets 1080px (~10× smaller);
  WebP/AVIF cuts 30–50% more; video autoplays muted at 480p and caps its
  bitrate ladder. Right-sizing + AVIF takes 2B impressions/day from ~150 KB
  to ~80 KB — half the bill for the same product. Transcode compute is paid
  once per upload; egress is paid forever — always optimize for smallest
  bytes.
- **Deliveries: serve only what is seen.** Lazy-load media as it enters the
  viewport (feed pages render 20, users see ~5); thumb-first, full image on
  expand; immutable keys + `max-age=31536000` make repeat views free from the
  browser cache. Do not fragment the cache key with auth or tracking
  parameters.
- **Hit ratio:** misses are what reach the origin, and 95% → 99% hit cuts
  miss traffic 5×. Origin shielding, long TTLs, warming for predictable
  viral spikes.
- **$ per GB:** multi-CDN (CloudFront + Fastly + Cloudflare) behind a traffic
  steer for committed-use pricing; keep origin and CDN in the same cloud
  (S3→CloudFront origin egress is free; cross-cloud pays twice).
- **Non-user traffic:** hotlink protection / tokenized media URLs, WAF and
  bot filtering, per-URL rate limits — scrapers ride your invoice.
- **Guardrails:** budget alarms on GB/day per media type. The most common CDN
  cost spike is not growth; it is a bug that started serving originals into
  the feed.

## 7. Engagement (Likes, Comments, Reposts)

- Writes are rows in `likes`/`comments` — cheap, idempotent on the primary
  key, and the source of truth.
- The count is the hard part: a celebrity post's `like_count` is among the
  hottest rows in the database — thousands of `UPDATE`s/s on one row is a
  row-lock convoy. Standard hot-key treatment:
  `INCR likes:{post_id}` in Redis (atomic, ~100K ops/s per node) with a
  periodic flush job writing the delta to `posts.like_count`. Display-only,
  so seconds of drift are acceptable.
- Comments have the same shape as posts (append + counter) nested under a
  post via `comments_post_idx`.
- Notifications are fan-out again — a smaller cousin of §4, pushed to the
  author's notification list, batched and collapsed ("you and 1,203 others
  liked…").

## 8. Privacy Controls

Private accounts and blocking, enforced **at both ends** — defense in depth:

- **Private accounts:** a follow creates `status = 'pending'`; the owner
  approves. Fan-out workers push only to `accepted` followers, so a private
  post never enters a stranger's precomputed feed.
- **Read-time filter — the safety net:** hydration batch-checks
  `author.is_private`, follow status, and `blocks` (small per-request cache)
  and filters before response. This catches the races fan-out filtering
  cannot: public→private flips with stale pushed IDs, approval revocations,
  reposts. Fan-out filtering is the optimization; read-time filtering is the
  guarantee.
- **Blocking:** read-time only. A block must take effect instantly, and
  retroactively scrubbing Redis feeds would be expensive and still racy; the
  hydration filter makes blocked content vanish at next render.

Interview line: privacy is enforced where it is cheap to enforce often
(fan-out) and where it is authoritative (read), because either alone fails a
specific race.

## 9. Ranking

- **MVP: reverse-chronological.** Correct, explainable, and already the
  ordering of the snowflake-ID feed cache. Ship it.
- Evolution: **candidate generation** (the follows-graph feed from §4,
  optionally plus trending inserts) → **scoring** (recency decay, author
  affinity from engagement history, media presence, engagement velocity) →
  **safety valves** (chronology floor, max consecutive posts per author,
  "you're all caught up").
- Architecturally, ranking is a re-ordering service between feed fetch and
  hydration. Everything in §4 stays; that is why the feed machinery is built
  before ML is added to it.

## 10. Failure Modes & Bottlenecks

- **Redis feed-cache loss:** feeds are a materialized view of Postgres —
  rebuildable, so degradation, not outage. Fall back to pull-on-read (§4,
  attempt 1 — slow but correct) while feeds rebuild **lazily on first
  access**. An eager rebuild is a self-inflicted thundering herd on Postgres.
- **Fan-out lag:** viral posts propagate over seconds; celebrity posts are
  pull-by-design. Users notice feed staleness far less than feed slowness —
  bias toward available-and-stale.
- **Count drift:** Redis flush lag wobbles like-counts; acceptable because
  display-only, with the row tables as truth.
- **Duplicate delivery** (worker retries): post IDs dedupe at the §4 merge;
  duplicate list entries are harmless.
- **Why not shard Postgres (yet):** ~800 writes/s and a few TB/year do not
  justify it. The ladder: indexes → read replicas → Redis caching →
  partitioning (done, §3) → shard by `author_id` when a measured threshold
  says so. Premature sharding trades joins and transactions for operational
  pain with no measured win.

## 11. Requirement → Mechanism Map

| Requirement (§1) | Mechanism |
|---|---|
| Post text + media | `posts` + `media`, pre-signed uploads (§5) |
| Follow / unfollow | `follows`, asymmetric by design (§3) |
| Feed p95 < 300 ms | Hybrid fan-out: Redis feeds + celebrity pull merge (§4) |
| Like / comment / repost | Row tables + Redis counters with flush (§7) |
| Private accounts | `follows.status` + push-time filter + read-time safety net (§8) |
| Blocking | Read-time hydration filter (§8) |
| Uploads async | Direct-to-S3 upload + resize workers + state machine (§5) |
| 100:1 read:write | All amplification async in workers; synchronous path O(1) (§2) |

## 12. Trade-offs & Interview Notes

- **Open with the write:read asymmetry and derive the architecture from it**
  — do not assert components; show why each exists.
- **Name the celebrity problem unprompted** and land the hybrid conclusion:
  ~100K threshold, no push for celebrities, read-time merge, and the
  shared-timeline refinement (`celeb_posts:{id}` — one cached copy of the
  author's timeline beats 10M per-follower copies).
- **Pre-signed uploads + CDN** — media never touches an API server; bytes and
  cost live in the storage/CDN tier.
- **No distributed transaction with blob storage, so none is faked:** a
  Postgres state machine with ordering invariants, idempotent retries via
  deterministic keys, and a reconciler/GC. The one true transaction
  (readiness + ownership + insert) lives entirely in Postgres.
- **Defense-in-depth privacy** with the race each layer catches.
- **Decline to shard, with arithmetic** — the ladder before sharding, and the
  thresholds that would eventually justify it.
- **Ranking last:** reverse-chronological MVP, ML as a re-ordering stage over
  the candidate generator the rest of the doc already built.
