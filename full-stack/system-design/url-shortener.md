# URL Shortener — Design Document

Design a URL shortening service (TinyURL / bit.ly class): a user submits a
long URL and receives a short, unique URL; anyone following the short URL is
redirected to the original. The service must scale to thousands of requests
per second, support custom aliases, track clicks for analytics, and stay
highly available. Assumed scale: ~100M new links/month, ~10B redirects/month.
Out of scope for v1 (each is a delta, not a redesign — see section 12):
per-customer custom domains, link-in-bio pages, QR generation.

> **Core insight — reads outnumber writes ~100:1, and the business is the
> click data.** Three consequences drive the whole design: (1) the redirect
> path is a cache-served key lookup that must never touch the OLTP database
> when warm, (2) redirects are **302, not 301**, so every click is observed,
> and (3) click capture is asynchronous — analytics never sits on the redirect
> critical path. One framing decision before any engineering: a short code is
> a *name*, not a hash of content — analytics requires two different codes
> for the same long URL (campaign tracking), so content-derived codes are
> wrong at the requirements level before they are wrong at the engineering
> level.

## 1. Requirements & Scale

**Functional**

- `shorten(long_url, custom_code?, expiry?) → short_url`, code ≤ 7 chars
- `redirect(code) → long_url` at low latency
- Custom aliases (vanity URLs)
- Click analytics: counts, geo, device, referrer, time series
- Link expiry and deletion

**Non-functional**

- Redirect p99 < 50 ms regionally; 99.9%+ availability on the redirect path
- Links effectively live forever — a short URL is embedded in the world;
  losing rows breaks signage everywhere
- Read-your-own-writes: create → paste → first click must resolve
- Abuse resistance: rate limiting, malware screening

**Back-of-envelope scale**

| Metric | Assumption | Number |
|---|---|---|
| Writes (new links) | 100M/month | ~40/s avg, ~400/s peak |
| Reads (redirects) | 100:1 read:write | ~4K/s avg, **~40K/s peak** |
| Storage | ~500 B/row (URL + code + metadata + index) | 50 GB/month → **~3 TB / 5 yr** |
| Cache | top ~20% of recent links | single-digit GB → 95%+ hit rate |
| Egress | ~1 KB per redirect response | ~40 MB/s peak — modest |

The punchline: this is **not** a big-data problem. The load is a
point-lookup key-value workload that a cache tier absorbs trivially, and the
dataset is single-digit terabytes after five years. The hard parts are code
uniqueness, keeping analytics off the hot path, redirect availability, and
abuse — not raw scale. The classic interview trap here is proposing Hadoop
and aggressive sharding for a 3 TB / 5-year dataset.

## 2. High-Level Architecture

Three paths, deliberately drawn separately — they have different latency
budgets, different availability requirements, and different scaling levers:

```
REDIRECT PATH (hot, read — ~40K QPS peak)
─────────────────────────────────────────────────────────────
browser ──GET /aB3xK9z──▶ LB ──▶ app ──1 get(code)──▶ Redis
                                         │              │
                                         │    hit ──▶ 302 + Location ──▶ browser
                                         │
                                         2 miss ──▶ MySQL shard (hash(code))
                                                        │
                                         3 row ──▶ app fills Redis, returns 302

SHORTEN PATH (cold, write — ~400 QPS peak)
─────────────────────────────────────────────────────────────
client ──POST /api/urls──▶ LB ──▶ app
                                    │ validate URL + code (section 8)
                                    ├──4──▶ INSERT into MySQL shard
                                    │        unique index arbitrates the claim
                                    └──5──▶ warm Redis (read-your-writes:
                                             create → paste → first click hits)

ANALYTICS PATH (async, off the critical path)
─────────────────────────────────────────────────────────────
app ──after the 302 is sent──▶ Kafka ──▶ enrichers ──▶ ClickHouse ──▶ dashboards
```

Components:

- **Load balancer / app tier** — stateless, N instances across AZs, scaled
  horizontally. No sticky state anywhere above the data stores.
- **Redis cluster** — `code → (long_url, expires_at, flags)` cache, consulted
  first on every redirect. Cache-aside: the **app** misses to MySQL and the
  **app** fills Redis — Redis never talks to MySQL. This keeps the cache
  non-authoritative and replaceable (see section 10 for failure handling).
- **MySQL shards** — durable source of truth; shard key is deterministic in
  the code (section 5). Reached only on cache miss and on shorten.
- **Kafka → ClickHouse** — the entire analytics business, strictly
  downstream of the response (section 9).

## 3. Entry Points: Anycast LB and GeoDNS

What vanilla costs: normal DNS gives **one answer for everyone**, and a
normal load balancer balances across backends **in one region**. A user in
Singapore hitting a us-east entry point pays the full transpacific RTT on
every redirect — against a 50 ms p99 budget.

- **GeoDNS** — the authoritative DNS server varies its answer by the
  client's approximate geography (US resolvers → US entry IPs, EU → EU IPs);
  routing at the DNS layer. Caveats: geography is inferred from the
  *resolver's* IP (public resolvers muddy this; EDNS Client Subnet fixes
  most of it), and failover is bounded by DNS TTL — minutes, not seconds.
- **Anycast** — one IP announced via BGP from multiple locations
  simultaneously; internet routing delivers each user's packets to the
  network-nearest announcer. Proximity at the routing layer, faster
  failover (withdraw the announcement), incidental DDoS spreading. Caveat:
  if BGP shifts mid-TCP-connection the connection breaks — harmless for a
  one-request HTTP redirect.

Beyond proximity, the real addition over a normal LB is the **failover
story**: a single-region entry point makes region death equal service death;
GeoDNS/anycast make region failure survivable. Honest scoping: at 4K avg /
40K peak QPS, one region with a managed LB works fine — the geo entry
points buy regional latency and regional failover, and are an "add when
global, not day-one" decision.

## 4. Short Code Generation — Random + Unique Index + Bounded Retry

Three cooperating parts, each covering a weakness of the others:

| Part | Provides | What it costs |
|---|---|---|
| Random 7 chars | No coordination (no counter service), non-enumerable, uniform keys → even shards | Collisions are *possible* |
| Unique index | The actual uniqueness guarantee — collisions become *impossible to miss* | One failed insert on collision |
| Bounded retry | Turns "rare collision" from an error into a routine branch | ~nothing (math below) |

The framing that matters: **randomness makes collisions rare, the database
makes them impossible to miss, the retry makes them harmless.** Uniqueness
is not probabilistic — the index enforces it; probability only governs how
often the retry branch runs.

```python
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase  # 62
CODE_LEN = 7            # 62^7 ≈ 3.5 × 10^12 codes
MAX_ATTEMPTS = 5

def allocate_code(long_url: str) -> str:
    for _ in range(MAX_ATTEMPTS):
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))
        try:
            insert_row(code=code, long_url=long_url)   # unique index arbitrates
            warm_cache(code, long_url)                 # read-your-writes
            return code
        except DuplicateKeyError:                      # MySQL error 1062
            continue                                   # fresh draw — expected
    raise CodeSpaceExhausted                           # alert; never expected
```

- Each attempt is an **independent fresh draw** — that is what makes the
  retry math valid. Retrying the *same* code would be an infinite loop by
  definition.
- The INSERT is a single-statement transaction: on duplicate, nothing was
  written and there is no partial state. The cache warms only on success,
  so a race loser never pollutes Redis.
- "Base62" here names the alphabet, not the encoding. A counter-based
  id → base62 is *reversible* (decode the code → recover the row); a random
  string is not — the code must be stored and indexed. That is a real cost
  of random, and the reason section 6 lays the table out physically for
  code lookups.
- Length: 7 chars over 62 gives ~3.5 × 10^12 codes; at 100M/month the
  5-year occupancy is 6B codes ≈ 0.17%. A case-insensitive alphabet (51
  chars) would need 8 chars for the same headroom — keep 62 and accept the
  minor dictation/print UX cost.

**Collision math (why the bound can be 5).** Collision probability per
attempt is occupancy: `p = codes_in_use / 62^7`; attempts-to-success is
geometric with expectation `1/(1−p)`:

| Codes in use | Occupancy | P(collide) | P(all 5 attempts collide) |
|---|---|---|---|
| 6B (~5 years at 100M/month) | 0.17% | 0.17% | ~1.4 × 10⁻¹⁵ |
| 350B (~290 years) | 10% | 10% | 1 × 10⁻⁵ |
| 1.76T (half the keyspace) | 50% | 50% | 3% |

Expected attempts at year 5: ~1.002. The retry branch fires about once per
600 inserts, and a bound of 5 carries the design safely past half the
keyspace — centuries of headroom.

**The subtleties that make it sound:**

- **CSPRNG is load-bearing.** `secrets` (i.e. `os.urandom`), never
  `random` (Mersenne Twister): an attacker who observes ~624 outputs of a
  seeded MT recovers its state and predicts every *future* code — enabling
  link squatting and enumeration of newly created links. The
  "random codes resist enumeration" claim rests entirely on RNG
  unpredictability.
- **Concurrency is handled, not hoped away.** Two servers can draw the same
  code simultaneously; both INSERT; the index rejects exactly one; it
  retries with a fresh draw. No distributed lock, no pre-check.
- **Custom codes share the insert but not the retry.** A 1062 on a
  *user-chosen* code means "that name is taken" → surface `409` with
  suggestions. Only *machine-generated* codes retry invisibly. One claim
  path, two collision policies (section 8).
- **The bound exists to catch systemic breakage, not collisions.** Things
  that could make every attempt fail: keyspace genuinely exhausted, the
  unique index accidentally dropped, or — the nasty one — two app versions
  disagreeing on the shard hash, so each checks a different shard and each
  per-shard check stops being a global check → silent duplicates. A bounded
  loop converts all of these into an alertable failure instead of an
  infinite spin. State the invariant: *per-shard unique = global unique
  only while every writer routes identically* (section 5).

**Alternatives, declined or deferred:**

| Strategy | Uniqueness | Enumeration risk | Verdict |
|---|---|---|---|
| Hash of URL, truncated + probe | Collisions → probe loop | None | Couples code to content — wrong for analytics (core insight); deterministic probing serializes on hot URLs |
| Auto-increment counter → base62 | Guaranteed | **High** — sequential codes let anyone walk the entire link graph (a real bit.ly problem) | Needs counter infrastructure; declined |
| **Random + unique index + bounded retry** | Index-enforced | None | Chosen: simplest correct thing |
| Counter + format-preserving permutation (Feistel) | Guaranteed | None | The polished upgrade if retry loops offend — counter uniqueness with random-looking codes |

## 5. Sharding — Deterministic by Code, over Logical Buckets

Generation and sharding are separate mechanisms that compose:

```text
generation:  code = 7 uniform CSPRNG chars over a 62-char alphabet
sharding:    bucket = xxhash64(short_code) % 1024
             physical_shard = bucket_map[bucket]     # ops-owned mapping table
```

A fast non-crypto hash (xxhash64; fnv1a also fine) is deliberate — we need
uniformity, not collision resistance; MD5/SHA work but buy nothing.

**Why the composition is sound — the elegant part:** a random code could
collide globally, but sharding is *deterministic by code*, so any two racers
inserting the same code land on the **same shard**, where the per-shard
unique index arbitrates. The per-shard unique index *is* a global uniqueness
guarantee — no distributed lock, no coordination service (see section 4 for
the writer-routing invariant that keeps this true).

**Why `hash(code)` beats the alternatives as shard key:**

| Shard key | Redirect lookup | Write spread | Verdict |
|---|---|---|---|
| `hash(short_code)` | 1 shard, point read | Uniform (random codes) | ✅ the hot query *is* the shard key |
| `id` (monotonic) | code→id needs an extra hop or scatter | **Hot last shard** (all inserts append) | ❌ |
| `creator_id` | Scatter across all shards | Skewed to big accounts | ❌ dead on arrival |
| `hash(long_url)` | Works, but campaign-duplicate URLs break the invariant | Uniform | ❌ couples sharding to content |

**Resharding.** Naive `% N` remaps every key when N changes (anti-pattern).
The 1024-logical-buckets indirection means growing 4 → 8 physical shards
*moves buckets*: only 1/N of keys relocate, and the mapping table is the
only thing that changes. Consistent-hashing rings solve the same problem
differently; the directory approach is easier to reason about and is what
Vitess-style systems do.

**Anti-premature-sharding note, same stance as the flash-sale doc:** at
3 TB / 5 yr, a single MySQL primary + read replicas fits for years. Start
with one physical shard (the bucket map makes that a table entry, not a
redesign) and add shards on measured thresholds — sustained insert rate,
maintenance windows, replica lag — not forecasts.

## 6. Data Model & Index Design

```sql
create table urls (
  short_code varchar(7) not null,
  long_url varchar(2048) not null,
  creator_id bigint null,
  created_at timestamp default current_timestamp,
  expires_at timestamp null,
  is_deleted boolean default false,
  primary key (short_code),
  key idx_creator_created (creator_id, created_at),
  key idx_expires (expires_at),
);  -- sharded: bucket = xxhash64(short_code) % 1024 (section 5)
```

**Why the code is the primary key — one descent, not two.** InnoDB is a
B+tree engine: a balanced search tree whose nodes are whole 16 KB pages
holding hundreds of keys, with all data in the doubly-linked leaf level.
The practical consequence for a 6B-row table: a ~350-way fanout gives height
≈ 4, the root and upper levels are a few pages permanently resident in the
buffer pool, and a point lookup costs 1–2 uncached page reads. A binary tree
over the same keys is depth ~32 — thirty-two pointer chases, each
potentially a page fault. Because the PK *is* the table (the clustered
index), `primary key (short_code)` makes a redirect **one** B+tree descent
into a leaf that already holds `long_url` and `expires_at`. A surrogate `id`
PK would make `unique(short_code)` a secondary B+tree whose leaves store the
id → every redirect pays *two* descents (find id, then fetch row). At a
100:1 read:write ratio the table is physically laid out for the read.

Cost of that call, named honestly: a random clustered key scatters inserts
across leaf pages → page splits and worse buffer-pool locality than a
monotonic id. This matters at 40K *writes*/s; we have ~40/s avg, ~400/s
peak. Cheap.

**Secondary indexes — each earns its keep:**

- `idx_creator_created (creator_id, created_at)` — "my links" dashboard:
  equality on the leftmost column, `ORDER BY created_at DESC` range on the
  second (walked via the linked leaves, scanned backward for DESC). Bonus:
  secondary-index leaves store the PK, which is now `short_code` — so
  listing a user's codes is **covering** without fetching rows.
- `idx_expires (expires_at)` — serves only the nightly archival sweep
  (`expires_at < now()`, a bounded range over a sparse column). Never on
  the redirect path; expiry is checked from the cached row (section 7).
- **No index on `is_deleted`** — a low-cardinality boolean alone is
  uselessly selective; it is a residual filter after the row is in hand.
- Optional `url_hash binary(32)` index — only if the product wants "same
  user + same URL returns the existing code." `long_url` cannot be indexed
  directly: `varchar(2048)` utf8mb4 = 8 KB, over the 3072-byte index prefix
  limit — hash it.

All indexes are per-shard, and that is sufficient — again because sharding
is deterministic by code (section 5).

**Engine choice.** MySQL (familiar ops, transactions for code claiming)
with **DynamoDB/Cassandra as the honest alternative** — this is a pure
key-value workload with no joins and no secondary access patterns on the
hot path. LSM-based stores trade read amplification for write throughput we
do not need. Pick MySQL for v1; the schema and access patterns port
cleanly if the platform argument ever wins.

## 7. Redirect Path — the Hot Path

1. `GET /{code}` → app checks Redis → **hit**: return `302 + Location`
   immediately. The database is not on the warm path, ever.
2. Miss → point lookup on the correct shard → fill cache (multi-hour TTL,
   lazy refresh) → return 302.
3. **Read-your-writes:** creation does insert + cache warm in the same
   request (step 5 of the shorten path), so "create, paste, click 3 seconds
   later" always hits cache and never sees replica lag.
4. **301 vs 302:** 301 gets cached by browsers and proxies, cutting load
   but blinding analytics — *a cached 301 is a click we never see*. Clicks
   are the revenue → serve 302.
5. **Hot keys** (one viral link hammering a single Redis node): an
   app-tier micro-cache (1–5 s TTL) absorbs the bulk; hot-key replication
   across cache replicas absorbs the rest.
6. **Stampede control:** single-flight per code on TTL expiry (one
   in-process lock refetches, others wait) or probabilistic early
   expiration.
7. **Negative caching** (brief "not found") plus per-IP rate limits blunt
   random-code scans — defense in depth; a miss is already a cheap indexed
   no-op.
8. **Expiry is lazy:** `expires_at` travels inside the cache entry →
   expired links serve a branded `410 Gone` from the cache check itself.
   A nightly sweep (via `idx_expires`) archives expired rows to cold
   storage. Deletion/expiry work is never synchronous on a redirect.

## 8. Custom URLs — Business Flow

1. Client `POST /api/urls {long_url, custom_code: "my-promo"}` with auth.
2. **Auth → quota check.** Custom codes are the scarce, abuse-prone
   resource — per-account limits (e.g., 100/day, paid-tier gated) *before*
   any validation work.
3. **Validate `long_url`:** scheme http(s), ≤ 2048 chars, no embedded
   credentials (`user:pass@`), not on the domain blocklist.
4. **Validate `custom_code`:** `^[a-zA-Z0-9_-]{4,30}$`, not reserved
   (`api`, `login`, `admin`, `www`, `static`, …), minimum length 4 so
   customs cannot eat the short namespace.
5. **Claim — the crux.** One `INSERT` into `urls`; the unique index is the
   arbiter:
   - **Success** → commit, warm Redis, return `201 {short_url}`.
   - **Duplicate** → `409 Conflict` + suggested variants (`my-promo-2`,
     `get-my-promo`).
   - Why not check-then-insert: two racers both see "available," both
     insert, one silently owns the code and the other's URL points at
     someone else's link. The failed insert is optimistic concurrency —
     the race loser pays exactly one dead insert, no locks held.
   - **The symmetry:** custom and random codes share this single claim
     path — for random codes the "custom string" is just the generator's
     output, and the ~0.17% collision retry is the same `DUPLICATE KEY`
     branch. One mechanism, not two; they differ only in collision policy
     (409-and-report vs retry-invisibly, section 4).
6. **Post-accept, async:** Safe Browsing scan of a newly-seen `long_url` →
   if flagged, redirects serve an interstitial warning page instead of the
   302, creator notified.
7. **Redirect of `my-promo`** is byte-identical to any code's path:
   cache → 302 (section 7).
8. **Lifecycle decisions that surface here:** codes are immutable (no
   rename — it would break every embedded instance and split analytics
   history); deletion is soft (`is_deleted` → branded `410 Gone`); expiry
   is per-link, set at creation.

## 9. Analytics — Kafka → ClickHouse

One main topic, `clicks`, **keyed by `short_code`**, using Kafka's default
partitioner (`murmur2(key) % P`):

- **Why key = code:**
  1. **Even spread** — codes are uniformly random, so partitions
     load-balance by construction; no skew except genuinely viral links.
  2. **Per-code ordering** — all events for one link land on one partition
     in order, making sessionization and late/duplicate handling per link
     tractable.
  3. **State locality** — a stateful consumer (incremental per-code
     rollups) owns its codes without cross-partition shuffles.
- **The skew caveat, said out loud:** key = code caps a single link's
  events at one partition/consumer. A mega-viral link pushing beyond
  partition throughput backs up its partition while others idle. Since
  heavy aggregation lives in ClickHouse anyway, accept this; the escape
  hatch is splitting into an unkeyed raw-archive topic plus a keyed rollup
  topic.
- **Partition count:** 32–64. Peak 40K/s ÷ 64 ≈ 600/s per partition —
  comfortable headroom, and ~2–4× max consumer parallelism so scaling
  consumers never stalls on partition starvation.
- **Semantics:** retention 7 days (ClickHouse is the durable store; Kafka
  is a replay buffer); producer `acks=all` + idempotent; consumers
  at-least-once with dedup by `event_id` (e.g. ClickHouse
  `ReplacingMergeTree`). The async producer in the app spills to local
  disk if Kafka is unreachable — redirect latency never waits on a broker.
- **Enrichment lives downstream, not in the app:** consumers do IP→geo
  (MaxMind) and user-agent parsing, then batch-insert into ClickHouse.
  The redirect path stays dumb and fast.
- **Queries:** raw events + daily rollups per `(code, day, country,
  device)`; unique clicks via HyperLogLog (±1–2%, fine for a dashboard).
  Anti-pattern: `COUNT(DISTINCT)` over raw events at dashboard-query time.
  Live counters for viral campaigns: fire-and-forget `INCR` per
  `(code, day)` in Redis, sampled into ClickHouse.
- One small second topic, `link_lifecycle` (created/expired/deleted), so
  the analytics side can join dimensions without touching OLTP MySQL.

## 10. Availability & Failure Modes

The asymmetry is the design: **redirect availability ≫ shorten
availability.** A failed shorten is an inconvenience; a failed redirect
breaks every link currently in flight anywhere. Every degradation decision
follows from ranking those two paths (and analytics a distant third).

- Stateless app tier, multi-AZ, behind the section-3 entry points —
  horizontal scale, no sticky state.
- **Redis tier fails** → the app falls through to MySQL read replicas:
  40K QPS of point lookups across a replica set is survivable; p99
  degrades, the service lives. Shed analytics first. Because the cache is
  cache-aside and non-authoritative (section 2), there is no consistency
  work to do on recovery — it simply rewarms.
- **MySQL primary fails** → automated failover per shard; replicas keep
  serving redirects throughout; shortens retry or 503 for the window.
- Weekly-ish dependencies (Kafka, the nightly sweep) are buffered so their
  failure never touches the hot path.

| Failure | Blast radius | Mitigation |
|---|---|---|
| Redis cluster down | DB miss storm, latency spike | Fall through to replicas, admission control, app micro-cache |
| Viral hot key | One cache node saturates | App micro-cache (1–5 s), hot-key replication |
| Kafka down | Analytics delayed | Local disk spill + replay; redirects unaffected |
| Primary failover | Shortens fail for minutes | Replicas serve redirects throughout |
| Sequential-code enumeration | Full link-graph scraping | Random codes (section 4), rate limits |
| Malicious long URLs | Phishing under our domain | Validation, async Safe Browsing → interstitial + takedown |
| Replica lag on fresh links | New link 404s once | Cache warm at creation (section 7) |
| Shard-hash version skew | Silent duplicate codes | Per-shard unique stops being global → bounded-retry alert fires (section 4) |

## 11. Requirement → Mechanism Map

| Stated requirement | Mechanism |
|---|---|
| Unique and short URL | Random 62⁷ CSPRNG code + unique index + bounded retry (section 4) |
| Scalability to thousands of requests | Cache-aside hot path, stateless tier, geo entry points (sections 2, 3, 7) |
| Redirect from short link to original | 302 from cache, p99 < 50 ms, read-your-writes (section 7) |
| Custom URLs | Atomic insert-claim, validation, reserved list, quotas (section 8) |
| Analytics and click tracking | Async Kafka → ClickHouse, HLL uniques (section 9) |
| High availability and uptime | Path asymmetry, replicated cache/DB, graceful degradation (section 10) |

## 12. Trade-offs & Interview Notes

- **Open with the math**, then derive: "4K/40K QPS, 3 TB / 5 yr — this is a
  key-value lookup problem with an analytics business attached, not a
  big-data problem." Do not assert components; show why each exists.
- Lines worth saying verbatim: *"302, because a cached 301 is a click we
  never see."* / *"The short code is a name, not a hash."* / *"Analytics is
  async or it doesn't ship."*
- **The trap** is over-engineering scale: sharding-everything and
  stream-processing frameworks for a workload a cache and one primary
  absorb. The bucket indirection (section 5) exists precisely so the
  sharding answer can start at "one physical shard."
- **Uniqueness framing** earns credit: randomness makes collisions rare,
  the index makes them impossible to miss, the retry makes them harmless —
  and deterministic-by-code sharding is what turns a per-shard unique index
  into a global guarantee without coordination.
- Expected follow-ups, each a delta not a redesign: **expiry/TTL**
  semantics (already lazy, section 7); **custom domains** (uniqueness
  becomes `(domain, code)` — namespace the reserved list per domain);
  **rate limiting** (per-IP/per-account quotas on shorten — spammers love
  free shorteners); **geo/edge** (regional read replicas +
  stale-while-revalidate at the edge); **10× scale** (more shards, deeper
  cache — no architecture change).
