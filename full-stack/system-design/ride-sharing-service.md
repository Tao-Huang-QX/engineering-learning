# Ride-Sharing Service — Design Document

Design a ride-sharing service (Uber/Lyft class): passengers request rides
through an app and are matched with nearby drivers. The design covers both
passenger and driver workflows plus: payment processing, payment-method
encryption and storage, push notifications and in-app messaging, user/driver
databases (MySQL), data privacy and encryption, GPS and mapping, user reviews
and score aggregation, tracking to identify patterns and spikes, and an image
hosting system.

> **Core insight — three workloads, three consistency regimes.** The dominant
> write stream is driver locations (~75K writes/s), and it never touches a
> database: latest position lives in memory (Redis), history flows through the
> event log (Kafka). The marketplace itself — matching — is an in-memory,
> eventually consistent loop. Strong consistency is reserved for what demands
> it: ride facts and money, co-located in sharded MySQL so every fare commit
> is one local ACID transaction. Everything else (chat, ratings, analytics,
> surge) is event-driven off the same log.

## 1. Requirements & Scale

**Functional**

- Passenger: request a ride with upfront fare quote, track the driver on a
  live map, chat/call, pay automatically, rate and tip
- Driver: go online/offline, receive offers (accept/decline with timeout),
  navigate, complete trips, view earnings, manage documents
- System: match riders to nearby drivers, meter and charge fares, surge
  pricing, notifications in both directions

**Non-functional**

- Match latency: request → first driver offer **< 3 s p99**
- Availability 99.99% on the request/match path, with graceful degradation —
  a wider-radius match beats a failed request
- Payments: never lose or double-charge money (strong consistency,
  idempotency, append-only ledger)
- Everything else (chat delivery, rating updates, analytics) is eventually
  consistent

**Back-of-envelope scale** (mid-size: 5M DAU)

| Metric | Assumption | Number |
|---|---|---|
| Rides/day | | 2M → ~23/s avg, **~200/s peak** |
| Concurrent online drivers | | 300K |
| **Driver location writes** | every 4 s per driver | **~75K writes/s** |
| Nearby-driver geo queries | ~10× ride requests | ~2K/s (trivial for Redis) |
| Rides table growth | | ~730M rows/yr → must shard |
| Chat messages/day | 30% of rides × ~5 msgs | ~3M/day, ~270 GB at 90-day TTL |

The location write rate is the number that shapes the whole design: 75K/s
means driver locations can never land on the SQL primary.

## 2. High-Level Architecture

```
            ┌─────────────────────────────────────────────┐
            │                  CLIENTS                    │
            │   Passenger app · Driver app · Ops web      │
            └────────────────────┬────────────────────────┘
              HTTPS/REST         │  WebSocket (chat, live ride
                                   status, driver location)
            ┌────────────────────▼────────────────────────┐
            │   API GATEWAY — auth, rate limiting, WSS    │
            └────────────────────┬────────────────────────┘
  ┌────────────┬─────────────┬───┴─────────┬───────────┬────────────┐
  ▼            ▼             ▼             ▼           ▼            ▼
┌──────────┐┌───────────┐┌────────────┐┌───────────┐┌───────────┐┌─────────┐
│ Location ││ Matching/ ││   Ride     ││  Payment  ││ Chat &    ││ Rating  │
│ ingest   ││ dispatch  ││ lifecycle  ││           ││ notif     ││         │
└────┬─────┘└─────┬─────┘└─────┬──────┘└─────┬─────┘└─────┬─────┘└────┬────┘
     │            │            │             │           │           │
     ▼            ▼            ▼             ▼           ▼           ▼
  Redis GEO   Redis state   MySQL (rides,  MySQL ledger  DynamoDB    MySQL
  (positions)              sharded)      + PSP vault   + WS gateway (ratings)
     │            │            │             │           │           │
     └────────────┴──────┬─────┴─────────────┴───────────┴───────────┘
                         ▼
                   ┌──────────┐
                   │  KAFKA   │  domain events: locations, rides,
                   └────┬─────┘  payments, ratings, driver status
            ┌───────────┴────────────┐
            ▼                        ▼
   Flink / Spark Streaming     S3 lake (Parquet, partitioned
   · surge pricing signals     by dt/city)
   · spike/anomaly alerts            └─► warehouse (Snowflake/BigQuery)
   · live dashboards                       └─► dbt models, dashboards
```

**Pattern:** synchronous microservices for the request path; Kafka as the
event backbone for everything downstream. Each service owns its store (no
shared databases). Payments sit with rides on the same shard key (§5).

## 3. Core Workflows

**Ride state machine** (source of truth in MySQL, hot state cached in Redis):

```
REQUESTED → MATCHING → DRIVER_ASSIGNED → ARRIVING → IN_PROGRESS
          → COMPLETED → FARE_PROCESSED → RATED
MATCHING ──(timeout, no driver in radius)──► NO_DRIVER_FOUND / CANCELLED
FARE_PROCESSED ──(decline)──► RETRY → DUNNING / SUPPORT
```

**Driver workflow:**
`OFFLINE → ONLINE → AVAILABLE → OFFER (10 s timer) → EN_ROUTE → ARRIVED → ON_TRIP → AVAILABLE`

**Matching flow (the heart):**

1. Passenger confirms pickup → ride created (`REQUESTED`), quote attached,
   card pre-auth initiated
2. Matching service queries Redis GEO for drivers within ~2 km, expands the
   ring outward (H3 cells) if empty
3. Candidates scored by **ETA** (routing service), not straight-line distance
4. Sequential offers: best driver gets push + in-app prompt, 10 s to accept,
   then next driver; offer state tracked in Redis
5. Accept → `DRIVER_ASSIGNED`, both parties notified, WebSocket streams
   driver location to the passenger

**Greedy vs batch matching:** greedy (nearest driver, first-come) is simple
and fast but suboptimal in dense markets. Batch matching collects requests
over a 2–5 s window and solves a bipartite assignment minimizing total ETA
across all riders. Start greedy; introduce batching per-city when density
pays for the added latency.

## 4. Location & Matching

- Driver app sends location every 3–5 s while online, adaptively: higher
  approaching pickup, lower when idle (battery). Passenger location streams
  during an active trip (safety).
- **Location ingest service:** stateless, scales horizontally. Latest
  position → Redis (`driver:{id} → lat,lng,bearing`, TTL) plus Redis GEO for
  radius queries; full stream → Kafka for history and analytics.
- **Geospatial index:** Redis GEO (geohash-backed) answers "drivers near X"
  in memory. For polygon regions and multi-resolution rings use H3/S2 cells
  (Uber uses H3) — ring expansion for candidate search, city-level
  aggregation for analytics.
- **Routing/ETA:** OSRM/Valhalla self-hosted or Google/Mapbox managed. ETA
  feeds both the matching score and the upfront fare (route distance × rate
  + time × rate). Common split: managed APIs for fare-setting accuracy,
  cached/self-hosted for high-volume matching heuristics.
- Snap-to-road on client or ingest side; geofence triggers arrival
  ("driver within 50 m of pickup").

## 5. Ride Data: Storage & Sharding

Rides are the classic two-sided marketplace row: ~90% of writes key on
`ride_id`, but the two hot read paths key on the participants. A row lives
in exactly one shard — the shard-key choice is the whole game.

| Query | Frequency | Natural key |
|---|---|---|
| Ride lifecycle writes (~10 status updates per ride) | every ride | `ride_id` |
| Payment + ledger entries | 1–3 per ride | `ride_id` |
| Passenger: current ride + history | every app open | `passenger_id` |
| Driver: current trip + earnings | hot path + daily | `driver_id` |
| Ops: active rides per city | dashboards | `city_id` |

**Decision: shard by `region + hash(ride_id)`.**

```
create ride ──► rides row on shard hash(ride_id)      ← one local ACID txn
                (payments + ledger co-located: same shard key)
                │  async, idempotent (at-least-once)
                ├──► user_rides(passenger_id, ride_id, dt, city, fare, status)
                │        on shard hash(passenger_id)
                ├──► driver_rides(driver_id, ride_id, dt, fare)  [at match time]
                │        on shard hash(driver_id)
                └──► Kafka ride_events  (replayable source for repair)
```

Why `ride_id` wins:

- **It exists at insert time.** The ride is created before matching —
  `driver_id` is unknown for the first seconds. Sharding by driver forces a
  row migration at match. Disqualified.
- **Uniform distribution.** Hash of ride_id never skews; hashing by user or
  driver skews with entity celebrity (power users, full-time drivers).
- **Payments co-locate for free.** Fare + ledger writes commit with the ride
  state transition in **one local transaction** — money never spans a
  distributed transaction.

The entity read paths are solved with **skinny index tables**, sharded by
their own keys, with two refinements:

1. **Denormalize summary columns onto index rows** (dt, city, status,
   fare_cents) so "my trips" lists and the driver earnings dashboard
   (`SUM(fare_cents)`) are single-shard reads with zero fan-out. Only the
   trip-detail screen fetches the owning shard.
2. **The hot active ride never touches MySQL** — Redis
   `active_ride:{user_id}` → ride_id + status, TTL until terminal state.

**Index consistency:** writes are async at-least-once, deduplicated by
`UNIQUE(user_id, ride_id)` insert-if-absent, reconciled by a job diffing
Kafka's event log against the indexes. Staleness symptom = a trip missing
from a list for a few seconds — acceptable, because the index is an
optimization; the ride row + ledger on the home shard remain the source of
truth. Money never depends on a cross-shard index.

**Rejected alternatives:**

| Shard key | Verdict | Why |
|---|---|---|
| `passenger_id` | Workable, worse | Driver earnings (heaviest reader) scatter-gathers; heavy passengers skew |
| `driver_id` | Non-starter | Unknown at insert; row migration on match |
| `city_id` alone | Too coarse | NYC ≫ Omaha; one city's write ceiling caps the system |
| Scatter-gather everything | Never | p99 = slowest shard on every page load |

**Operations:**

- **IDs:** Snowflake/UUIDv7 — timestamp-prefixed, globally unique with zero
  cross-shard coordination, time-sortable for archival range scans. A global
  `AUTO_INCREMENT` is a distributed-transaction generator; reject it.
- **Rebalancing:** logical vshards ≫ physical servers (e.g., 4,096 logical →
  32 servers, consistent hashing maps vshard → server). Adding capacity
  moves vshards between servers; the `ride_id → vshard` mapping never
  changes. This is Vitess's model.
- **Bounding growth:** completed rides archive to the warehouse/cold storage
  after 6–12 months (in-shard partitions by `completed_at`; drop partition =
  instant eviction). ~12 months hot ≈ 2 TB → 32–64 shards at a comfortable
  30–60 GB each.
- **Honesty check:** 23 rows/s average is trivial for one beefy MySQL box.
  Sharding buys multi-region residency, write headroom, and independent
  failure domains — say so; the platform shards, not the feature.

## 6. Payments & Ledger

- **Pre-auth / capture:** pre-authorize the quote at match time (card hold)
  → meter/finalize fare at completion → capture; if final > hold, capture +
  one additional charge. Wallet balances checked at request time.
- **Idempotency keys** on every payment operation (webhooks are at-least-once).
- **Append-only double-entry ledger:** passenger debit, platform-fee credit,
  driver-payout credit. Never `UPDATE` amounts — corrections are new
  reversing entries.
- PSP webhooks → payment service → update ride payment status → emit
  `payment.captured` → receipt + driver earnings accrual.
- Daily **batch reconciliation** against PSP settlement files (Airflow DAG).
- Driver payouts settle daily in batch; failures feed a dunning flow (retry,
  fallback card, support queue).

## 7. Payment Methods: Tokenization & Encryption

- **Don't store card numbers — tokenize.** PSP (Stripe/Adyen/Braintree)
  vaults the card via their SDK components so the PAN never touches our
  servers. This shrinks PCI DSS scope to the lightest audit tier — the
  entire game. We store:

```sql
payment_methods(id, user_id, psp_customer_id, psp_token,
                brand, last4, exp_month, exp_year,
                fingerprint, is_default, created_at)
```

- **In-house sensitive data** (SSNs, license numbers): **envelope
  encryption** — KMS/HSM-backed master key never leaves the KMS; each record
  gets a data key encrypted by the master; payload encrypted AES-256-GCM
  with the record ID bound as AAD (prevents ciphertext swapping). Rotate
  masters by key version; re-encrypt lazily.
- Never log tokens or PANs; payment data in a separate schema on a segmented
  network.

## 8. Notifications, Chat & Transport

**Notifications are event-driven:** state-machine transitions publish to
Kafka (`ride-events`); the notification service renders per channel
(APNs/FCM with a device-token registry), retries with exponential backoff,
tracks delivery receipts. Never call APNs inline from the ride service — a
slow APNs call must not block matching.

**In-app chat:** WebSocket gateway cluster; Redis registry maps
`user_id → gateway node` so any node can route to a connected user.
Offline recipient → push notification with the payload. Reconnects use
jittered backoff so a gateway blip doesn't thundering-herd.

**Transport: WebSocket over TCP. Why not UDP.** The question is really about
transport, not layers — the service is application-layer either way.
Chat/notifications are reliable, ordered, low-rate streams (~100–500 ms
latency tolerance): exactly TCP's profile. Rolling your own reliability on
raw UDP = re-implementing TCP, worse. UDP earns its place only where loss is
tolerable:

- **Voice/video calls** (masked passenger↔driver calling): WebRTC/SRTP
- **High-rate location telemetry**, latest-value-wins with sequence numbers —
  defensible at 10 Hz rendering; in practice WebSocket at our rates keeps
  client code simple
- **QUIC (HTTP/3)** is the evolution path: UDP underneath with reliability
  rebuilt on top, and its **connection migration** survives a passenger's
  phone switching WiFi→LTE mid-ride — the ride-app-specific reason to care

**Chat persistence: DynamoDB.** The Cassandra-vs-DynamoDB question is a
cost-TCO framing trap at this workload — both are NoSQL wide-column; the
real choice is managed vs self-operated:

| Cost line (3M msgs/day, 90-day TTL) | DynamoDB (on-demand) | Self-hosted Cassandra |
|---|---|---|
| Writes (90M WRU/mo) | ~$110/mo | — |
| Reads (~270M RRU/mo) | ~$70/mo | — |
| Storage (270 GB) | ~$70/mo | cheap (instance storage) |
| Compute | $0 | 6–9 nodes × 3 AZs ≈ **$1–2K/mo** |
| Humans | $0 | repairs, ring ops, GC tuning |

~$250/mo total vs a cluster costing 5–8× that before the operator.
DynamoDB's expensive reputation comes from sustained high throughput on
on-demand pricing (~5–7× provisioned; fix with provisioned + reserved
capacity, not a database swap). Cassandra's real price for TTL-heavy chat:
**TTL deletion creates tombstones** — mass expiry without TWCS sized to the
TTL window causes compaction storms; "you must know to configure that" is
the cost. Cassandra wins with steady six-figure ops/s, a self-hosting
mandate, or true multi-DC active-active — our design pins a ride to one
region, so chat needs none of those.

## 9. Data Privacy & Encryption

- **In transit:** TLS 1.3 externally; mTLS between services (service mesh).
- **At rest:** volume-level AES-256 everywhere, **plus field-level**
  envelope encryption for high-sensitivity PII (phone, email, license #) and
  location history.
- **Access control:** RBAC + just-in-time unmasking — support sees masked
  phone by default; unmasking requires a ticket reason and writes an audit
  event. Query-level audit logs on PII tables.
- **Retention/deletion (GDPR/CCPA):** financial records legally retained
  (~7 y) — delete requests *anonymize*: null PII columns, keep the ledger
  row. Location traces: 30–90 days raw for product/safety, then delete or
  aggregate only.
- **Residency:** EU users' data pinned to an EU region — the region prefix
  in the shard key (§5) makes this physical, not procedural.

## 10. Ratings & Score Aggregation

- Mutual post-trip ratings; **hidden until both submit or 72 h passes**
  (prevents retaliation bias).
- Store rows per trip; aggregate incrementally — never `AVG()` over
  unbounded history:

```sql
ratings(ride_id, rater_id, ratee_id, rater_role, stars, comment, created_at,
        UNIQUE(ride_id, rater_role))

rating_aggregates(subject_id, avg_ewma, count_30d, count_total, updated_at)
```

- **Recency-weighted (EWMA) average**, updated by an event handler on each
  insert — O(1) reads for profile screens and matching eligibility.
- Thresholds (driver < 4.6 → quality program; < 4.2 → review) calibrated
  **per-city percentile** in the warehouse — a 4.5 in Manhattan isn't a 4.5
  in a suburb.
- Batch graph analysis catches rating rings/fraud.

## 11. Analytics: Patterns & Spikes

**Kappa-style pipeline:** all services emit events → Kafka (Avro/Protobuf +
schema registry, at-least-once with idempotent sinks). One replayable log
serves both streaming and batch — no dual lambda pipelines.

- **Streaming layer** (Flink / Spark Structured Streaming):
  - Demand/supply per `(city, H3 cell)` in 1-min tumbling windows → Redis,
    consumed by pricing and matching
  - **Spike detection:** compare the live window against a seasonal baseline
    (same-minute median of last 4 weeks + EWMA); z-score over threshold →
    `surge_pressure` event → pricing steps the multiplier; ops alert fires
  - Distinguish organic spikes (concerts, weather — join scheduled-event and
    forecast feeds) from incidents (check error rates first: a request spike
    may be a client retry storm)
  - Funnel health: request→match rate, match ETA p50/p95, offer acceptance
    rate per cohort
- **Batch layer:** Kafka → S3 Parquet (partitioned `dt/city`) →
  Snowflake/BigQuery → dbt models (GMV, utilization, driver churn),
  Airflow-orchestrated.

## 12. Image Hosting

- Types: avatars (public-ish), driver documents (license/insurance —
  strictly private), trip-issue photos.
- **Upload:** client gets a **pre-signed S3 PUT URL**, uploads directly to a
  private bucket (bytes never transit the APIs) → S3 event → async scan
  pipeline (malware + content moderation + face-match for driver identity)
  → on pass, thumbnail/resize lambda → metadata row flips to `approved`.
- **Serving:** avatars via CDN; documents only via short-TTL signed URLs to
  verified internal tools.
- **Strip EXIF** (embedded GPS is a privacy leak); size and content-type
  caps; face-crop avatars.

## 13. Data Model (sharded MySQL unless noted)

```sql
users(id, email_enc, phone_enc, name, created_at, deleted_at)
drivers(id, user_id, status, license_no_enc, bg_check_status, rating_avg)
vehicles(id, driver_id, plate, make, model, year)
payment_methods(...)                                    -- §7
rides(id, passenger_id, driver_id, status, pickup_lat, pickup_lng,
      dropoff_lat, dropoff_lng, surge_multiplier,
      requested_at, matched_at, started_at, completed_at,
      fare_quote_cents, fare_final_cents)               -- shard: hash(ride_id)
payments(id, ride_id, psp_payment_id, amount_cents, currency, status,
         idempotency_key UNIQUE, created_at)            -- co-located with rides
ledger_entries(id, account_id, ride_id, direction, amount_cents, reason,
               idempotency_key UNIQUE, created_at)      -- append-only
user_rides(passenger_id, ride_id, dt, city, status, fare_cents)  -- shard: passenger_id
driver_rides(driver_id, ride_id, dt, fare_cents)                 -- shard: driver_id
ratings(...) / rating_aggregates(...)                   -- §10
-- Chat: DynamoDB, key (ride_id, ts), 90-day TTL      -- §8
```

## 14. Scaling, Bottlenecks & Failure Modes

1. **Location ingest (75K/s):** stateless ingestion + Redis cluster sharded
   by driver; Kafka partitioned by city. Never the SQL primary.
2. **Matching hot loop:** partition the matching service by city (state in
   Redis); cities are natural isolation units.
3. **MySQL:** shard by `ride_id` with index tables per access path (§5);
   payments co-located.
4. **WebSocket gateway:** sticky routing via the Redis registry;
   degraded-mode read-only during reconnect storms.
5. **Multi-region:** active-active with geo-affinity — a ride lives entirely
   in its region; the financial ledger is single-writer per region with
   async cross-region replication.
6. **Graceful degradation:** routing service down → straight-line distance
   scoring; Redis GEO down → wider-radius cached fallback; a worse match
   beats a failed request.
7. **Payment failures:** retries idempotent by key; ambiguous states (network
   timeout to PSP) never auto-release; dunning + support queue.

**Monitoring:** match latency p99, offer acceptance rate, Redis↔MySQL
active-ride drift, index-table reconciliation lag, ledger↔PSP settlement
diff, surge pressure vs baseline, WebSocket reconnect rate.

## 15. Requirement → Mechanism Map

| Stated component | Mechanism |
|---|---|
| Passenger workflow | Upfront quote → match → WebSocket tracking → auto-pay → rate/tip (§3) |
| Driver workflow | Online/offline, 10 s offers, earnings dashboard off `driver_rides` (§3, §5) |
| Payment processing | Pre-auth/capture + append-only double-entry ledger + daily PSP reconciliation (§6) |
| Encryption & storage of payment methods | PSP tokenization (PCI scope reduction) + envelope encryption for in-house secrets (§7) |
| Push notifications & in-app messaging | Kafka-driven notification service (APNs/FCM); WebSocket gateway + Redis registry; DynamoDB + TTL (§8) |
| User/driver databases (SQL/MySQL) | Sharded MySQL: `region + hash(ride_id)`, index tables, Snowflake IDs, vshard rebalancing (§5) |
| Data privacy & encryption | TLS/mTLS, field-level envelope encryption, JIT unmasking + audit, anonymize-not-erase, regional pinning (§9) |
| GPS & mapping | Adaptive location ingest → Redis GEO / H3, ETA-scored matching, snap-to-road, geofences (§4) |
| User reviews & score aggregation | Mutual hidden ratings, incremental EWMA aggregates, per-city percentile thresholds (§10) |
| Data tracking for patterns & spikes | Kappa pipeline: Kafka → Flink windows vs seasonal baselines → surge + alerts; batch → lake → dbt (§11) |
| Image hosting | Pre-signed direct upload, async scan/moderation, CDN for avatars / signed URLs for docs, EXIF strip (§12) |

## 16. Trade-offs & Interview Notes

| Decision | Chose | Over | Because |
|---|---|---|---|
| Location store | Redis GEO + TTL + Kafka | MySQL/PostGIS | 75K writes/s; latest-only in memory |
| Geo index | H3 cells (+ Redis GEO) | raw geohash | ring expansion, multi-resolution |
| Dispatch | greedy + sequential offers | batch everywhere | latency first; batch where density pays |
| Rides/payments | sharded MySQL | Cassandra/DynamoDB | money needs ACID + auditable ledger |
| Ride shard key | `hash(ride_id)` + region | passenger/driver/city | exists at insert; uniform; payments co-locate |
| Chat messages | DynamoDB + TTL | self-hosted Cassandra | ~$250/mo vs 5–8× + an operator; managed TTL |
| Chat transport | WebSocket/TCP | raw UDP | reliable ordered low-rate; UDP only for voice/WebRTC |
| Ratings | incremental EWMA aggregate | on-demand AVG | O(1) reads, bounded storage |
| Cards | PSP tokenization | encrypt PANs ourselves | PCI scope reduction |
| Analytics | kappa (one Kafka log) | lambda (dual pipelines) | replayable, one pipeline to maintain |

**Three probes this design survived (with the answers that earned credit):**

1. *"Why not UDP for chat/notifications?"* — Layering correction first
   (UDP is transport; the service is application-layer either way), then:
   reliable ordered low-rate streams are TCP's profile; raw UDP means
   re-implementing TCP badly. UDP is right for WebRTC voice and latest-wins
   telemetry; QUIC is the evolution path because connection migration
   survives mid-ride network switches.
2. *"How do you shard ride data?"* — Access-path analysis first; one
   physical key (`hash(ride_id)` + region); index tables with denormalized
   summaries for the two entity paths; async idempotent writes reconciled
   from Kafka; vshards so keys never rehash; archive to bound growth.
3. *"Isn't Cassandra cheaper than DynamoDB?"* — Both are NoSQL wide-column;
   the real axis is managed vs self-operated. At 3M msgs/day DynamoDB is
   ~$250/mo; a minimum Cassandra ring costs 5–8× that in EC2 before the
   operator. Cassandra's tombstone/TWCS burden on TTL-heavy chat is exactly
   the hidden cost. Swap only for sustained six-figure ops/s, self-hosting
   mandates, or multi-DC active-active.
