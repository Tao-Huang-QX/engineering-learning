# Video Streaming Service — Design Document

Design a video streaming service (Netflix-shaped, not UGC-shaped): users
browse, search, and play video; **internal teams** upload content through a
back-end CMS, so the catalog is curated rather than crowd-sourced. The
service must scale to large audiences, support upload/storage/editing of
large media files, and cover the canonical components: MySQL user data, media
hosting, privacy/age controls, engagement (follow/like/comment/share),
performance recording, ranking/recommendations, notifications, and the
player. Assumed scale: ~50M MAU, ~10M DAU, ~100K hours of catalog. Out of
scope (named, not ignored): live streaming, billing, offline downloads (one
paragraph each in §15).

> **Core insight — bytes flow one way.** A streaming service is a broadcast
> network with a metadata application attached. ~27 PB of video leave the
> platform per day while the API tier moves kilobytes. Every decision below
> exists to (1) keep video bytes off the API tier, (2) make those bytes as
> small as per-title encoding allows, and (3) make them so cacheable that the
> ~10 Tbps evening peak is served entirely at the CDN edge — the playback
> path never calls home to a database.

## 1. Requirements & Scale

**Functional**

- Browse a catalog (home rows, category pages) and search titles
- Play video with adaptive quality; resume across devices
- Internal teams upload, edit, schedule, and take down content via CMS
- Engagement: like, comment, follow channels, share (deep links)
- Age restrictions, kids profiles, regional availability
- Personalized home page (ranking/recommendations)
- New-episode push notifications; service-wide announcements
- Record video performance (viewer analytics + streaming quality)

**Non-functional**

- **Startup < 2 s, rebuffer ratio < 0.5%** — playback QoE is the product;
  these are the binding constraints, and they are *measured*, not assumed (§11)
- Playback path survives backend outages (§13) — a database incident must not
  freeze every player mid-stream
- Read:write is extreme even by social-app standards; uploads are scheduled
  and predictable (curated catalog), which the ingest pipeline exploits (§4)
- Catalog consistency is eventually-consistent-friendly; entitlement decisions
  must be correct at token issuance (§10)

**Back-of-envelope scale**

| Metric | Assumption | Number |
|---|---|---|
| Watch time | 2 h per DAU/day | 20M hours/day |
| Avg delivered bitrate | ABR mix, minority 4K | ~3 Mbps |
| **Egress** | watch time × bitrate | **~27 PB/day; ~3M peak concurrent ≈ 10 Tbps** |
| Catalog | internal teams | ~100K hours, +10K hours/month |
| Serving storage | ~12 GB/hour full ladder | ~1.2 PB (masters ~5 PB, archive tier) |
| Plays | avg asset ~40 min | ~30M plays/day |
| Telemetry | ~30 player events/play | ~1B events/day (~12K/s avg) |
| Catalog/API reads | browse + search + recs | ~100M/day (~1.2K/s avg, 12K/s peak) |
| Social writes | likes/comments/follows | ~50M/day (~600/s avg) |

The shaping number is **egress**, and the second shaping number is the
**content ratio**: 10K hours uploaded per month vs ~600M hours delivered per
month — **each content-hour is uploaded once and watched ~60,000 times.**
Write:read ≈ 1:60,000. The system is a read-only broadcast with a factory
attached (§4), not an application with a video feature.

## 2. High-Level Architecture

```
                video segments (~27 PB/day, ~10 Tbps peak)
   Players ─────────────────────────────────────────────────> CDN (multi-CDN)
     │  HTTPS: API + signed manifests          miss            │
     │                                            └─ shield ─> S3 renditions/
     v                                              (coalesced) immutable segments
     LB ──> API services
     │       catalog / search / playback-auth /
     │       social / events-collector / notify
     │          │            │              │
     │          v            v              v
     │        MySQL      OpenSearch       Redis
     │       (truth)     (search, §7)     (counters, watch progress)
     │          v
     │        Kafka ──> stream processors ──> warehouse (§11)
     │                    └──> search indexer / notification workers (§7, §12)
```

Three consequences of this shape:

1. **The playback path is edge-autonomous.** Once a player holds a signed
   manifest (§5, §10), every segment fetch hits the CDN. MySQL, Kafka, and
   the API tier can all be down and streams keep playing; only *new* sessions
   are affected. This is deliberate and is the availability story (§13).
2. **The API tier moves metadata only.** Upload bytes go direct to S3 via
   pre-signed multipart PUTs; delivery bytes go through the CDN. No video
   ever crosses a service in the middle box.
3. **Everything multiplied is queued.** Transcoding, search indexing,
   counter flushes, notifications, and analytics all happen behind Kafka
   after the synchronous path returns — the synchronous path stays O(1) per
   request.

**Event backbone — who publishes what to Kafka.** Three producers, three
characters:

| Producer | Topic(s) | What |
|---|---|---|
| Events-collector API | `player.events` | Player telemetry: heartbeats, rebuffers, bitrate switches, session end. The volume producer (~12K/s avg) |
| S3 event notification (small bridge) | `ingest.raw-uploaded` | `object-created` on `raw/` = "the master arrived, start transcoding" |
| CDC connector (Debezium tails the MySQL binlog) | `mysql.videos`, `mysql.titles` | Row-change events: status `ready`/`published`/`retired`, rating changed |

The CDC row is the load-bearing one: workers *only* write MySQL, and the
"video published" event that drives search indexing (§7) and notifications
(§12) is *derived from the commit log*. The alternative — a worker writing
MySQL and then producing a Kafka event (dual write) — has no transaction
between the two systems: crash in the gap and MySQL says published while no
event ever fires. **The database is the source of truth; CDC makes it the
source of events, atomically.** Pipeline workers may publish advisory
progress events ("encode 60% done"), but never truth.

## 3. Data Model (MySQL)

MySQL per the requirement. The schema splits cleanly into a **catalog side**
(channels/titles/videos/renditions — small, read-heavy, written by internal
teams) and a **user side** (profiles/engagement/progress — large, written by
the audience). That split is the future shard boundary: the catalog fits one
primary + replicas for years (~1M video rows), while user-side tables can
shard by `user_id` when measured numbers say so.

```sql
create table users (
    id            bigint primary key,
    email         varchar(255) not null unique,
    password_hash text not null,
    birth_date    date not null,             -- drives age-band enforcement (§10)
    region        char(2) not null,
    created_at    datetime(3) not null default current_timestamp(3),
);

create table profiles (
    id             bigint primary key,
    user_id        bigint not null,
    name           varchar(40) not null,
    maturity_level smallint not null,        -- ceiling 0..5, compared to rating (§10)
    pin_hash       text,                     -- null = no lock on this profile
    is_kids        boolean not null default false,
    created_at     datetime(3) not null default current_timestamp(3),
);
create index profiles_user_idx on profiles (user_id);

create table channels (                      -- internal teams publish as channels
    id             bigint primary key,
    name           varchar(80) not null unique,
    owner_team     varchar(80) not null,
    follower_count bigint not null default 0,
    created_at     datetime(3) not null default current_timestamp(3),
);

create table titles (
    id                bigint primary key,
    kind              varchar(10) not null,  -- 'movie' | 'series'
    name              varchar(200) not null,
    synopsis          text,
    content_rating    smallint not null,     -- 0..5, aligned with maturity_level
    release_year      smallint,
    artwork           json,                  -- candidate thumbnails (§8)
    available_regions json not null,         -- geo licensing (§10)
    status            varchar(12) not null,  -- editorial lifecycle
    publish_at        datetime(3),           -- embargo: not before (§4)
    created_at        datetime(3) not null default current_timestamp(3),
);

create table videos (                        -- the playable asset (per episode)
    id            bigint primary key,
    title_id      bigint not null,
    season        smallint,
    episode       smallint,
    duration_secs int not null,
    master_key    text not null,             -- S3 raw/ object
    status        varchar(12) not null,      -- ingest state machine (§4)
    like_count    bigint not null default 0,
    comment_count bigint not null default 0,
    created_at    datetime(3) not null default current_timestamp(3),
);
create index videos_title_idx on videos (title_id, season, episode);

create table renditions (
    video_id  bigint not null,
    label     varchar(12) not null,          -- '240p' ... '2160p'
    bandwidth int not null,                  -- bits/s
    codec     varchar(20) not null,          -- 'h264', 'hevc', 'av1'
    uri       text not null,                 -- manifest-relative path
    primary key (video_id, label),
);

create table follows (
    profile_id bigint not null,
    channel_id bigint not null,
    created_at datetime(3) not null default current_timestamp(3),
    primary key (profile_id, channel_id),
);
create index follows_channel_idx on follows (channel_id);

create table likes (
    profile_id bigint not null,
    video_id   bigint not null,
    created_at datetime(3) not null default current_timestamp(3),
    primary key (profile_id, video_id),
);
create index likes_video_idx on likes (video_id);

create table comments (
    id         bigint primary key,
    video_id   bigint not null,
    profile_id bigint not null,
    body       varchar(2000) not null,
    status     varchar(10) not null default 'visible',  -- moderation state
    created_at datetime(3) not null default current_timestamp(3),
);
create index comments_video_idx on comments (video_id, created_at desc);

create table watch_progress (
    profile_id    bigint not null,
    video_id      bigint not null,
    position_secs int not null,
    completed     boolean not null default false,
    updated_at    datetime(3) not null,
    primary key (profile_id, video_id),
);
```

Modeling decisions:

- **`videos.status` is the ingest transaction** — the whole upload/transcode
  lifecycle's truth lives in one MySQL column, where real transactions exist;
  S3 has none (§4 expands this).
- **`content_rating` and `profiles.maturity_level` share one 0–5 scale**, so
  the age filter is a single integer comparison — cheap at query time, small
  enough to embed in a signed playback token (§10).
- **Normalize vs json, decided per column by a test**, not by habit.
  Normalize when elements have independent identity/lifecycle, direct
  row-level queries, or shared parents; keep json for value objects read and
  written whole with their parent. Applied:
  - `renditions` **passes the test and is a table** — the manifest minter
    queries it per video, packaging writes rungs incrementally as they
    complete, each rung has real per-row identity.
  - `titles.artwork` **stays json** — fetched as a set, rendered as a set,
    ordering is inherent to the array (a child table would need a `sort_key`
    to express it), elements are S3 keys that cannot be foreign-keyed anyway.
  - `titles.available_regions` **stays json, with a reason** — the per-title
    direction ("does this title include my region?") is a membership test on
    an in-hand row; the inverse direction ("titles for region DE") is served
    by OpenSearch, which denormalizes regions as a filter field regardless of
    what MySQL does (§7). MySQL never issues that query, so the index a
    normalized table would buy serves no code path. The answer flips to
    normalize if regions gain independent lifecycle (per-episode, dated
    license windows) or if the search layer did not exist.
  - The transcode **ladder *plan*** (rungs chosen by the complexity pass) is
    pipeline state — it matters between analysis and packaging, then it is
    done — so it lives in the orchestrator's job store, not in the catalog.
    `renditions` records what was actually produced.
- **`watch_progress` is the one hot table.** 3M concurrent players emitting
  heartbeats is ~300K events/s — never a synchronous MySQL write, and not
  even dependent on Kafka: Redis-first with a consumer flush (§11).
- **Counters denormalized** (`follower_count`, `like_count`, `comment_count`),
  maintained out-of-band via Redis + flush (§9). Never `count(*)` on a read
  path.
- **`titles` vs `videos` separation**: the catalog/marketing entity (what you
  search and recommend) is distinct from the playable asset (what transcodes
  and streams). A series is one title, many videos.

## 4. Ingest Pipeline — Upload, Store, Edit (the offline factory)

Internal upload changes the problem vs UGC: ingest volume is scheduled and
predictable (season drops, not a firehose), and creators are trusted
(internal SSO), so there is no moderation gate — but there *is* an editorial
one, and an embargo to respect (§10). Nothing in this pipeline is on the
playback path.

```
   CMS ──> ingest API: create videos row (status='uploading')
    │        + presigned multipart PUT (resumable, 100 MB parts)
    │                                 │
    │  bytes, direct                  v
    └────────────────────────────> S3 raw/   (immutable master, ~50 GB–1 TB)
                                     │ object-created event → Kafka
                                     v
                        transcode orchestrator
                        1. probe + complexity pass → pick ladder plan
                        2. split master into 2–6 s GOP-aligned segments
                           → fan out parallel encode jobs (FFmpeg workers)
                        3. package HLS + DASH manifests, encrypt each
                           rendition (AES-128 + Widevine/FairPlay/PlayReady)
                        4. thumbnails, sprite sheet (scrubbing), auto-preview
                                     │
                                     v
                     S3 renditions/{video}/{label}/{segment}.ts
                                     │
                                     v
            MySQL: uploading → uploaded → transcoding → ready
                    → (editorial review, metadata/artwork/rating) → scheduled
                    → published (flips automatically at publish_at)
```

**Ordering invariants** (two stores, no cross-store transaction — the state
machine is the transaction):

- **a) The `videos` row exists before any bytes move.** An abandoned upload
  is always a findable row, never anonymous S3 spend. A reaper deletes
  `uploading` rows older than 7 days, and an S3 lifecycle rule aborts
  incomplete multipart uploads — parked parts bill as storage.
- **b) Nothing is playable until `ready`.** Manifests are only minted against
  `ready`+ videos, so a feed can never render a dead player.
- **c) Deterministic keys make retries idempotent.** Segment keys are
  `video_id + label + index`, so a worker crash mid-ladder re-runs and
  overwrites itself.
- **d) Published segments are immutable.** Immutability is the cache-key
  contract (§5); edits never mutate bytes in place (below).

**Crash points, enumerated** — the honest version of "guaranteed":

| Crash point | Leftover state | Recovery |
|---|---|---|
| Client abandons upload | `uploading` row, partial parts | Reaper + S3 lifecycle abort |
| Worker dies mid-encode | partial segments, `transcoding` | Reconciler re-enqueues; keys overwrite idempotently |
| Renditions complete, crash pre-UPDATE | objects on disk, still `transcoding` | Retry re-packages only; cheap |
| Scheduled but never published | `scheduled` past `publish_at` | Publisher cron flips status; embargo held by tokens (§10) |
| Takedown after publication | `retired` | Tokens stop being minted; existing tokens age out in minutes |

**Editing large files** splits into two very different operations:

- **Metadata edits** (title, synopsis, artwork, rating, regions) are MySQL
  updates — instant, no bytes touched.
- **Byte edits** (re-cut, re-master) create a **new asset version**: transcode
  a fresh rendition set, atomically flip the manifest pointer in MySQL, let
  old segments age out of CDN caches under their old immutable keys, then GC.
  In-place mutation would poison every cache simultaneously.

**Transcode sizing**: ~8 compute-hours per content-hour across a full ladder.
10K hours/month ≈ a few hundred vCPUs average — trivial — but a 10-episode
season drop is ~80 compute-hours, which 480 workers finish in ~10 minutes.
The fleet is queue-backed and auto-scaled; scheduling drops in advance makes
the load predictable, which is the quiet gift of the internal-upload model.

## 5. Delivery — CDN + Adaptive Bitrate

How ~3M concurrent streams get served without a 10 Tbps origin fleet. Taught
as a progression; each step's failure motivates the next.

**Attempt 1 — one MP4 per title, served from origin.** 3M concurrent ×
3 Mbps = 9 Tbps from one fleet. Dead on arrival. Worse: progressive download
ships bytes nobody watches (average session is a fraction of the asset), a
seek re-ranges a multi-GB file, and one bitrate fits nobody's network exactly.

**Attempt 2 — a CDN in front of the MP4s.** Origin egress collapses to cache
misses — real progress. But the file still cannot *adapt*: a phone on a 1 Mbps
link cannot smoothly play a 6 Mbps 1080p file, and a 4K TV forced down to a
single low bitrate looks terrible. Quality changes mean downloading a
different entire file. The unit of caching (whole file) is also the unit of
adaptation (none).

**Concluded — adaptive bitrate (ABR) streaming.** Each title is transcoded
into a *ladder* of renditions (240p ≈ 0.4 Mbps → 4K ≈ 16 Mbps), cut into
2–6 s GOP-aligned segments, described by a manifest (HLS/DASH). The player
measures its own throughput and buffer and requests a different rendition
per segment (§6). Three structural wins:

- **Every segment is an immutable, independently cacheable object**
  (`renditions/{video}/{label}/{segment}`). Hot segments — the first minutes
  of a hit show — saturate edge caches; hit ratio climbs above 99% and the
  origin only sees the long tail.
- **Egress = Σ(viewer × sustained bitrate)** — viewers self-select the
  cheapest acceptable rendition instead of all paying the file's price.
- **The unit of caching is now the unit of adaptation** — 2–6 seconds.

**Per-title encoding** — the biggest cost lever after the CDN itself. The
first pipeline pass (§4) measures spatial/temporal complexity and picks the
ladder per title: a static dialogue-driven drama is perceptually transparent
at 1080p/3 Mbps, so its ladder is shallower; an action film keeps the 4K/16
Mbps rungs. Netflix's published figure is ~20% average bitrate saving at
equal perceived quality. Transcode compute is paid once per upload; egress is
paid per view, forever — always spend compute to shrink bytes.

**Origin protection — premieres are flash crowds.** A drop at 00:00 means
millions of players requesting the *same first segments* simultaneously:
perfect cacheability, zero warm cache. Three layers: (1) **origin shield** —
a mid-tier CDN tier that collapses concurrent identical misses into ~one
origin fetch per shield pop; (2) **pre-warming** — push the first N segments
of scheduled drops to edges before `publish_at` (the embargo is enforced by
tokens, §10, so warming early leaks nothing); (3) **multi-CDN with per-player
steering** — sessions are assigned a CDN by measured health, and the QoE
telemetry (§11) closes the loop on which CDN is actually performing.

**Cost = deliveries × bytes × $/GB**, and each term has a named control:
bytes → per-title encoding + codec migration (AV1/HEVC cut 30%+ at equal
quality); deliveries → prefetch what will be watched, nothing more (§6);
$/GB → multi-CDN committed-use pricing, same-cloud origin (S3→CloudFront
origin fetches are free; cross-cloud pays twice).

**The auth-vs-cache subtlety:** manifests and segments are protected by signed
URLs (§10), but a per-user token in the query string would fragment the cache
key into uselessness — ten million viewers hold ten million different tokens
but fetch the *same* bytes. Resolution: **validate the token at the edge,
exclude it from the cache key** (CloudFront signed URLs/cookies, or an edge
function) — access control and cacheability are separate concerns and must be
configured separately. Getting this wrong is the classic streaming cost bug.

## 6. Video Player

The player is a distributed-systems component: it is the ABR decision engine,
the telemetry source (§11), and the failover client.

- **Startup:** fetch manifest → begin two segments below the throughput
  estimate (conservative start beats a stall; quality steps up in seconds) →
  first frame rendered. Budget: < 2 s. A preloaded manifest for the top home
  row cuts this further.
- **Steady-state ABR:** throughput estimate = sliding window over the last
  K segment downloads; buffer occupancy is the guardrail — below ~10 s of
  buffer, drop a rung immediately; above ~30 s with headroom, step up one
  rung. Never jump multiple rungs (oscillation looks worse than a low
  bitrate). This is the buffer-based family of algorithms (BOLA et al.) in
  plain words.
- **Prefetch:** next segments speculatively at the current rendition; during
  end credits, prefetch the next episode's manifest and first segments
  (autoplay continuity is an engagement metric, §11).
- **Resume:** read `watch_progress` (Redis-first, §11) at manifest time; write
  on pause/exit/heartbeat.
- **Scrubbing:** thumbnails come from a sprite sheet — one image per video, a
  grid of frames every ~10 s — fetched once, cacheable forever, instead of a
  stream of thumbnail requests.
- **Multi-track:** alternate audio/subtitle renditions are manifest entries;
  switching tracks is a manifest re-selection, not a new session.
- **Error recovery:** on a failed segment, skip it (players tolerate a gap),
  drop a rung, back off exponentially, report to telemetry. On a 403
  (expired token), refresh the token and resume — tokens age out mid-session
  by design (§10).
- **Data saver / caps:** per-profile bitrate ceilings — the same profile
  machinery as age restrictions (§10) carries a bandwidth knob for free.

## 7. Search

- **OpenSearch cluster** indexing titles, channels, and people, denormalized
  with `content_rating` and `available_regions` from MySQL. Updates flow from
  the CDC event stream (§2); eventual consistency in minutes is fine — search
  is discovery, not truth.
- **Entitlement is a query-time filter, never an afterthought:** the same
  maturity/region predicates from §10 apply as filters, so a kids profile's
  search can never surface — even as a blurred count — an ineligible title.
  (This layer is also why MySQL never needs the inverse region query, §3.)
- Typeahead from a prefix index; popularity boost (from §11 telemetry) ranks
  canonical titles above long-tail matches with similar names.

## 8. Ranking & Recommendations

- **MVP: editorial + trending rows.** Internal teams already curate (that is
  what the CMS is for); trending is computed from the §11 pipeline. Correct,
  shippable, and already personalized-ish by region.
- **Architecture: the home page is rows, and rows are candidate sources.**
  Each row is an independent generator: *continue watching* (from
  `watch_progress`), *because you watched X* (item similarity),
  *popular in your region* (telemetry), *new from channels you follow*
  (`follows` + publish events), *editorial picks* (CMS). A ranking service
  scores candidates (affinity, recency decay, popularity, freshness), dedupes
  across rows, and applies safety valves (max consecutive items per series,
  diversity floors).
- **Personalized artwork:** the `titles.artwork` candidates (§3) exist because
  thumbnail CTR differs wildly by user segment — same title, different
  thumbnail. Cheap personalization with outsized effect.
- **Offline/online split:** training (matrix factorization / two-tower
  embeddings on watch history from the warehouse) runs offline on Spark;
  a feature store + model registry serves online scoring against
  Redis-cached features. Materialized home pages per user, recompute every
  few minutes or on signal (a finished episode retriggers "recommended").
  Home page reads are O(cached list), never model inference per request.
- **Cold start** (new title, new user): telemetry-derived trending +
  editorial placement + category affinity from early interactions.

## 9. Engagement (Follow, Like, Comment, Share)

Same shapes as any social system; listed with only what is specific here:

- **Follows** attach to channels (internal teams), driving the *new from
  channels you follow* row (§8) and publish notifications (§12). Fan-out is
  bounded by followers, batched by workers.
- **Likes are rows + the hot-counter treatment.** `UPDATE videos SET
  like_count = like_count + 1` on a hit video means thousands of UPDATEs/s on
  one row — they serialize behind the row lock while connections pile up (the
  row-lock convoy). Instead: `INCR likes:{video_id}` in Redis (atomic,
  in-memory, ~100K ops/s per node); a flusher atomically reads-and-resets
  (`GETSET likes:{video} 0`) and applies the delta as **one MySQL write per
  key per flush interval**. The `likes` rows are the source of truth (unlike
  is idempotent on the primary key; counts rebuild exactly via `count(*)` if
  Redis is lost); the counter is a display-grade materialized aggregate with
  bounded, self-healing drift. Same pattern for `comment_count`,
  `follower_count`, and view counts.
- **Comments** on curated content are still public UGC and need moderation:
  a spam/abuse classifier scores on write, reports queue to a moderation
  tool, `comments.status` hides pending/removed. Volume is bounded by the
  catalog's shape (no upload button → no viral comment storms on fresh
  content), but the machinery is mandatory.
- **Shares** are deep links (`/watch/{video}?t=90`) plus an OpenGraph meta
  endpoint so link previews render. No server-side fan-out.

## 10. Privacy, Age Restrictions & Entitlement

Age restrictions and regional licensing are the same mechanism — an
**entitlement predicate** `(profile.maturity_level ≥ title.content_rating) ∧
(region ∈ title.available_regions) ∧ (status = published)` — enforced at
three layers, because each layer catches a different hole:

1. **API/catalog/search filter (the listing guarantee).** Catalog queries and
   search filters (§7) apply the predicate in the query — ineligible titles
   are never listed, counted, or blurred-into-view for that profile. Kids
   profiles (`is_kids`) additionally hard-exclude comments/likes (children's
   privacy rules).
2. **Signed playback token (the bytes guarantee).** The playback-auth service
   checks the predicate and mints a short-TTL (minutes) token — a signed URL
   whose claims bind `{profile, video, max rendition, region, expiry}`,
   validated at the CDN edge, excluded from the cache key (§5). The split
   that makes it work: the *decision* happens once per play with database
   access; the *enforcement* happens per request with none — signature
   verification is pure CPU at the edge, which is why 3M concurrent streams
   never touch MySQL for authorization (§13). Each claim closes a hole:

   | Claim | What it enforces |
   |---|---|
   | `ProfileId` + `MaxLabel` | a kids profile on an adult account still cannot fetch adult renditions — the ceiling travels with the token |
   | `Region` | geo-licensing fails at the edge, even for a leaked URL |
   | `Expires` (minutes) | takedowns and rating changes take effect within minutes; URL sharing dies on the same clock; no tokens minted before `publish_at`, so pre-warmed segments (§5) leak nothing |
   | `Signature` | claims cannot be forged or edited (delete `MaxLabel`? no) |

   Mid-session expiry is a player feature, not a surprise: on 403 the player
   refreshes the token and resumes (§6).
3. **DRM license server (the last line).** Widevine/FairPlay/PlayReady
   licenses are issued only after the same entitlement check — segments are
   encrypted, so they are useless without a license regardless of URL
   leakage. The token gates *fetching* bytes; the license gates *decoding*
   them. Token stops link sharing; DRM stops stream saving.

Supporting details: `birth_date` on `users` establishes the account-level age
band; per-profile `maturity_level` + `pin_hash` implement parental controls
(the PIN gates upgrading maturity or leaving a kids profile); a rating change
is caught by three clocks — listings fix immediately (layer 1), live sessions
cap out when tokens expire (layer 2), and copied files never existed (layer
3). Interview line: privacy is enforced where it is cheap (query filters) and
where it is authoritative (edge tokens, DRM), because either alone fails a
specific race.

## 11. Recording Video Performance

One pipeline serves three masters: **product analytics** (what is watched),
**streaming QoE** (how well it plays), and **internal-team dashboards** (how
*their* content performs). The same events feed all three.

**Player → events-collector → Kafka → stream processors → warehouse.** Players
batch events (session start, rebuffers, bitrate switches, 10 s heartbeats,
errors, session end). ~1B events/day (~12K/s avg) is modest for Kafka; no
sampling needed. Aggregates land in ClickHouse-style serving stores for
dashboards; raw events land in Parquet on the lake as training data (§8) with
30–90 day retention.

- **QoE metrics are the SLOs**: startup p90 < 2 s, rebuffer ratio < 0.5%,
  average bitrate, error rate — sliced per title, per CDN, per POP. The
  per-CDN/per-POP slice is literally the input to multi-CDN steering (§5):
  telemetry does not just observe the system, it *operates* it.
- **Engagement analytics**: completion curves (where viewers abandon — the
  intro-skip pattern is famous), watch time by region/demo, thumbnail CTR
  (drives §8 artwork choice).
- **Channel dashboards**: because uploaders are internal teams, the warehouse
  serves them per-channel views/watch-time/completion reports — the
  "recording data about video performance" requirement read from the
  creator's side too.
- **`watch_progress` rides this pipeline — with one deliberate split.** The
  collector writes Redis synchronously (`SET progress:{profile}:{video}`)
  *because resume is playback* and must not depend on Kafka (the rule below);
  it publishes the heartbeat to Kafka asynchronously. A stream processor
  collapses to latest-per-key and flushes MySQL once per flush interval (or
  on `session_end`), and computes `completed` **server-side** (position ≥ 90%
  of duration) — players crash before sending, and a client that reports its
  own completion is a client that will eventually lie. Failure read: Redis
  lost → resume degrades to MySQL (stale by ≤ one flush interval); Kafka
  lost → resume keeps working in Redis while flushes lag. Both are
  degradations, not outages.

**Design rule: the analytics path is never coupled to the playback path.**
If Kafka or the collector degrades, players keep playing and events are
dropped best-effort — losing a day of dashboards beats losing a day of
streams.

## 12. Push Notifications & Announcements

Notifications produce **two artifacts with different fan-out economics**: the
*inbox* (the list you see on app open) and the *push send* (the device wake
via APNs/FCM — the vendor pipes that are the only way to reach an app that
isn't running). Treat them separately.

**The inbox is a mailbox, computed at read.** The criterion: is the audience
a *stored fact* or a *derivable predicate*?

- **Intrinsically addressed events** (a reply to your comment) get per-user
  rows — the event exists *about* one person; volume is proportional to 1:1
  interactions.
- **Predicate-defined events** (new episode from a followed channel) are
  computed at read: `follows ⋈ videos published > cursor`. No per-user
  writes, no 10M-row storm when a mega-channel drops, and the follow/unfollow
  race fixes itself — unfollow simply stops returning that channel, where a
  pre-pushed row would linger.

```
app open, profile P, cursor = last_seen:
  1. rows: notifications where profile_id = P      ← intrinsic events
  2. pull: followed channels ⋈ publishes > cursor  ← predicate events
  3. pull: announcements active for P's segments   ← broadcast rows
  merge, sort by time, render; badge = count
```

This is the feed fan-out lesson one level over — *don't copy what you can
compute cheaply at read* — with a cleaner criterion than a follower
threshold: a feed must be precomputed for speed (hence hybrid push/pull), but
a notification list is opened occasionally and tolerates a query, so
*everything* predicate-shaped is computed.

**The push send is inherently per-device.** APNs/FCM APIs are addressed per
token; there is no broadcast primitive at APNs. The row fan-out is
eliminable; the send fan-out is managed:

- **Scheduled drops → scheduled fan-out.** The audience is precomputed and
  sends are **staggered by timezone** across ~30–60 min. The mitigation *is*
  the feature: quiet hours mean EU users should not be woken by a 00:00 PT
  drop anyway — constraint and product requirement point the same direction.
- **"New season of a series you finished"** — the audience
  (`watch_progress.completed`) is a **warehouse query** (§11 already computes
  completion). Segment → campaign → send: computed offline, fanned out
  batched, never an analytical query against production MySQL.
- **Collapse keys + per-profile daily caps** from the preference center —
  "3 new episodes," retries idempotent via collapse keys. Device tokens are
  pruned on vendor invalid-token feedback; delivery is best-effort with no
  receipts, so engagement is measured by app opens (telemetry), not push
  acknowledgments.
- **FCM topic messaging for mega-channels:** devices subscribe to
  `channel:{id}` topics at follow time; one topic send fans out at Google's
  side, replacing 10M individual sends. Trade-off: topic sends cannot honor
  quiet hours or caps — reserved for the opted-in big-drop tier.

**Announcements are broadcasts, never fan-out writes.** A service-wide
banner is one row with an audience predicate and a validity window; clients
fetch `/announcements?since=` on app open. Writing 50M per-user rows to say
"scheduled maintenance" is the anti-pattern.

| Event | Inbox representation | Push send |
|---|---|---|
| Reply to your comment | per-user row (write) | direct send |
| New episode, followed channel | computed at read (mailbox) | staggered + collapsed; topics for mega-channels |
| New season of finished series | computed at read | warehouse segment → batched campaign |
| Announcement | broadcast row (pull) | at most one silent data-message ping |

## 13. Failure Modes & Bottlenecks

- **Edge POP or CDN failure:** multi-CDN with per-session steering (§5);
  players hold a CDN fallback list and re-request on failure. This is the
  only failure class that directly touches streams, and it is engineered
  around rather than "monitored".
- **MySQL down:** *playback does not stop* — tokens are edge-validated, not
  database-validated (§10); in-flight sessions continue, resumes fall back to
  Redis-then-MySQL, new sessions degrade to Redis-cached trending/editorial.
  The token design *is* the HA story.
- **Origin overload at a premiere:** shield + request coalescing + pre-warm
  (§5); drops are scheduled, so the load is predicted, not survived.
- **Transcode backlog:** priority lanes (takedowns first, then scheduled
  drops, then backfill) + auto-scale; a missed embargo-window is escalated,
  a slow backfill is not an incident.
- **Telemetry pipeline down:** best-effort loss, dashboards go stale,
  playback unaffected — the decoupling rule from §11. Resume survives too,
  because the collector's Redis write (§11) is synchronous.
- **DRM license server outage:** the one small stateful service on the
  playback path — new sessions fail, existing licenses persist for their
  cached duration; it gets aggressive HA (multi-region, hot spare).
- **Hot title, cold everything:** the celebrity problem, translated — solved
  structurally by segment-level caching (every viewer of a hit converges on
  the same thousands of immutable objects) rather than per-user machinery.
- **MySQL growth ladder:** replicas → Redis caching → partition engagement
  tables by time → shard user-side tables by `user_id` (the §3 boundary).
  Catalog tables shard never (or last).

## 14. Requirement → Mechanism Map

| Requirement (§1) | Mechanism |
|---|---|
| View + search videos | Catalog API + OpenSearch with entitlement filters (§7) |
| Internal back-end upload | CMS + pre-signed multipart + `videos` state machine (§4) |
| Upload/store/edit/transmit large files | Direct-to-S3 masters, segment parallelism, versioned asset swap, HLS/DASH over CDN (§4–5) |
| User data (MySQL) | Catalog/user split schema, replicas-then-shard ladder (§3, §13) |
| Video + image hosting | S3 renditions + CDN, thumbnails/sprites as cacheable artifacts (§4–5) |
| Privacy + age restrictions | Aligned rating scale, profiles + PIN, edge-validated signed tokens, DRM (§10) |
| Engagement | Follows/likes/comments rows + Redis hot counters + moderation queue (§9) |
| Recording video performance | Player telemetry → Kafka → warehouse; QoE as SLO + steering input (§11) |
| Ranking + recommendations | Row-based candidate generators + scoring service + feature store (§8) |
| Push notifications + announcements | Computed mailbox inbox + tamed per-device send fan-out; announcements as broadcast rows (§12) |
| Video player | Buffer-based ABR, prefetch, resume, sprite scrubbing, token refresh (§6) |
| Highly scalable | Edge-autonomous playback, immutable segment caching, async everything (§2, §5) |

## 15. Trade-offs & Interview Notes

- **Open with the egress math** (27 PB/day, 10 Tbps peak, 1:60,000 content
  ratio) and derive the architecture from it: CDN-first, API-as-metadata,
  factory offline. Do not assert components; show why each exists.
- **Name the internal-upload consequence early**: predictable ingest (no
  moderation firehose, schedulable transcode, pre-warmable premieres) but
  embargoes and per-title quality as first-class requirements. This is the
  sharpest contrast with a YouTube-shaped answer.
- **Playback autonomy is the availability story**: tokens validated at the
  edge mean a full backend outage cannot stop streams already playing. Say
  this sentence explicitly.
- **Validate tokens at the edge, exclude them from the cache key** — the
  auth-vs-cache subtlety. Forgetting it is the classic streaming cost bug.
- **The database is the source of truth; CDC makes it the source of events**
  (§2) — the dual-write problem named and declined.
- **Normalize vs json by test, not habit** (§3): renditions pass the
  normalization test; artwork/regions are value objects; MySQL doesn't
  normalize for queries that OpenSearch serves.
- **Hot counters** (§9): rows for truth and idempotency, Redis for hot
  arithmetic, a GETSET flusher to reconcile, nothing on a read path ever
  does `count(*)`.
- **Notifications: mailbox inbox, tamed sends** (§12) — per-user rows only
  for intrinsically addressed events; predicate audiences computed at read;
  the per-device send fan-out (APNs/FCM) staggered, collapsed, and
  topic-messaged.
- **Per-title encoding with the compute-once/egress-forever framing.**
- **Three-layer entitlement** (listing filter → signed token → DRM license),
  each layer named with the race it catches.
- **Live streaming, if asked, is a delta not a redesign**: the manifest/
  segment/CDN machinery is identical; the transcode factory becomes a
  real-time packager producing segments as the event happens, DVR is a
  sliding cache window, and latency budgets tighten. Offline downloads are
  DRM licenses with persistence plus local storage — no new backend service.
- **Decline to shard MySQL with arithmetic** — ~1M catalog rows and ~600/s
  social writes are years from needing it; the user/catalog split keeps the
  option cheap when it arrives.
