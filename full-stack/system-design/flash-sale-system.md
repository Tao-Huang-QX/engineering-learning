# Flash Sale System — Design Document

Design an eCommerce flash sale system: a hot product goes on sale at a fixed
time, demand is expected to exceed stock, each user may buy exactly one unit,
there is no cart (direct buy), and orders are fulfilled first-come-first-serve.
The product must read "out of stock" the moment the last unit is claimed, and
the purchase decision must return immediately while fulfillment continues in
the background.

> **Core insight — the queue is for processing, not deciding.** Since stock is
> a small known number and each user buys at most one unit, the system can
> decide admission at the front door in O(1). Only accepted requests ever
> reach the queue, the DB, or the payment service.

## 1. Requirements & Scale

**Functional**

- Sale starts at a fixed time; no purchases before T0
- Direct buy (no cart), **one unit per user**, enforced
- First-come-first-served; "out of stock" the instant demand exceeds supply
- Accept/reject decision returns immediately (frontend loader stops fast)
- Order fulfillment (payment, confirmation, notification) continues in the
  background after the response

**Non-functional**

- **No oversell** (never sell unit 100,001), minimal undersell
- Admission decision latency < 100 ms under burst
- Availability through a 10–100× traffic spike
- Downstream systems (orders, payments) must survive the spike

**Back-of-envelope scale**

- Stock: 100,000 units
- 1M users arrive at T0 → ~1M requests in the first 30–60 s, peak ~100K RPS
  in second one
- Ingress bandwidth is trivial (~20 MB/s of tiny POSTs). The hard parts:
  (a) one serialized decision per request, (b) the thundering herd,
  (c) protecting the DB and payment service

## 2. High-Level Architecture

```
            ┌────────────┐
 Users ───▶ │  CDN       │  sale page (static, cached)
            └─────┬──────┘
                  ▼
            ┌────────────┐   rate limit, auth, sale-start gate
 Users ───▶ │ API Gateway│──────────────────┐
            └─────┬──────┘                  │ rejected ─▶ 429/403/"not started"
                  ▼                         ▼
            ┌──────────────────┐    ┌───────────────────────┐
            │  Purchase API    │───▶│ Redis (admission gate)│
            │ (stateless, N)   │    │ Lua: admit or reject  │
            └─────┬────────────┘    └───────────────────────┘
                  │ admit: enqueue + return order_id (PENDING)
                  ▼
            ┌────────────┐
            │  Kafka/SQS │  (≤ stock messages, ever)
            └─────┬──────┘
                  ▼
            ┌──────────────────┐   1. final dup check
            │ Order Workers    │──▶2. durable stock decrement (txn)
            │ (consumer group) │   3. create order (PENDING_PAYMENT)
            └─────┬────────────┘   4. payment (async, TTL hold)
                  ▼
            ┌────────────┐      ┌─────────────┐
            │ PostgreSQL │      │ Notification│─▶ push/email "order confirmed"
            │ orders/inv │      └─────────────┘
            └────────────┘
```

Two consequences of the admission-gate design make everything downstream work:

1. **Downstream work is bounded at O(stock)** — at most 100K requests ever
   reach the queue, DB, and payment service, whether 1M or 100M requests
   arrive. A 100K-message queue drains in seconds.
2. **FCFS is decided at admission**, by the serialization point of the atomic
   counter — not by queue consumption order, so the queue can be partitioned
   freely for throughput.

The naive alternative (enqueue everything, let workers decide while draining)
fails the requirements: loaders spin for minutes, users rage-click, the queue
grows unbounded, and an instant "no stock" error is impossible.

## 3. Admission Gate (hot path, ~1 ms)

One Lua script in Redis — atomic, so it is the FCFS serialization point:

```lua
-- KEYS[1]=admitted  KEYS[2]=user_set  KEYS[3]=stock_key
-- ARGV[1]=user_id
if redis.call('SADD', KEYS[2], ARGV[1]) == 0 then
    return 'DUPLICATE'                    -- one-per-user, also dedupes retries
end
local admitted = redis.call('GET', KEYS[1]) or 0
local released = redis.call('GET', 'released') or 0
if tonumber(admitted) - tonumber(released) >= tonumber(redis.call('GET', KEYS[3])) then
    redis.call('SREM', KEYS[2], ARGV[1])
    return 'NO_STOCK'                     -- instant reject, no queueing
end
redis.call('INCR', KEYS[1])
return 'ADMIT'
```

`released` counts admitted requests that later failed (payment declined,
fraud hold, TTL expiry) and had their unit returned — it re-opens admission
for latecomers while the sale is live (see section 5).

Purchase API behavior per outcome:

| Outcome | Response | Frontend |
|---|---|---|
| `ADMIT` | `200 {order_id, status: PENDING}` — enqueue to Kafka, done. ~5–20 ms total | Stop loader, show success |
| `NO_STOCK` | `409 {error: "no_stock"}` — never touches the queue or DB | Stop loader, show error, **remove product from list** |
| `DUPLICATE` | `409 {error: "already_purchased"}` (return existing order_id) | Stop loader, show existing order |
| Before T0 / after end | `403` | Button disabled |

**Sold-out broadcast:** when `admitted − released` first reaches stock,
publish `SOLD_OUT` (Redis pub/sub → websocket push / CDN cache purge) so every
client flips to sold-out immediately — globally, not just for the user whose
request was the unlucky one.

**Scaling the hot key:** one product = one counter = one hot Redis key. A
single Redis node does ~100K ops/s on this script, which covers the estimated
load. Beyond that:

- **Stock bucketing** — split 100K stock into 1,000 keys of 100 each;
  admission picks a random bucket, retries another on empty; a global counter
  still drives the instant-reject decision
- **Edge waiting room** — hand out numbered tickets at the CDN/gateway layer
  before T0, admit users at a controlled rate; trades strict FCFS precision
  for graceful degradation

## 4. Order Workers (cold path, bounded at O(stock))

Per message from Kafka:

1. **Re-validate** — user hasn't ordered (DB unique constraint on
   `(user_id, sale_event_id)` is the final guard), sale is still valid
2. **Durable decrement** in one transaction:

```sql
UPDATE inventory
SET reserved = reserved - 1
WHERE sale_event_id = %s AND reserved > 0;   -- 0 rows ⇒ reclaim, increment released
```

3. **Create order** `status = PENDING_PAYMENT`, **hold stock with a TTL**
   (e.g., 15 min)
4. **Payment** asynchronously. On success → `CONFIRMED` + notify the user.
   On decline or TTL expiry → release the hold, increment `released`
   (see section 5)

Because at most 100K messages ever exist, this pipeline is sized comfortably:
50 workers at 200 msg/s each drain the whole sale in ~10 s, and the DB sees
≤100K writes total instead of 1M+.

The `order_id` returned to the user represents an *admitted*, not *shipped*,
order — the id comes back immediately in `PENDING` state and confirmation is
asynchronous ("Order placed, complete payment by 12:15").

## 5. Released Units: Reopening After Failed Purchases

When an admitted request fails definitively, its unit goes back on sale. The
gate condition `admitted − released < stock` reopens admission automatically —
new requests flow through the exact same path (Lua gate → Kafka → worker →
conditional decrement). No separate leftover-stock queue or special mode.

Four design decisions around that mechanism:

**a) Release only on definitive failure, exactly once.** Never release on
ambiguous states (network timeout to the payment provider — the charge may
still have landed); wait for explicit decline, fraud rejection, or hold-TTL
expiry. Make release idempotent: the worker transitions the order
`PENDING_PAYMENT → RELEASED` as a guarded state change
(`UPDATE ... WHERE status = 'PENDING_PAYMENT'` affecting exactly one row) and
increments `released` only if that transition succeeded. Worker retries must
not double-release — double-release over-admits, which the DB guard catches
but converts into "sorry, your confirmed order failed" apologies.

**b) Announce the restock.** The `SOLD_OUT` broadcast already removed the
product from every page; if nobody believes they can buy, released units sit
unsold. On `admitted − released` crossing back below stock, publish
`RESTOCKED` on the same channel so frontends re-enable the button.

**c) Debounce the flapping.** Fast declines (2–5 s) land while the herd is
still slamming, producing `SOLD_OUT → RESTOCKED → SOLD_OUT` churn. Buffer
releases and broadcast only when meaningful (≥ N units or every 30 s), or
gate all releases into a **scheduled second round**: collect releases for
15 min (letting TTL holds expire), then open a short announced window
("restock at 12:15"). The scheduled round converts flapping into a
controlled mini-event and is what real flash sales usually do.

**d) Who gets the released unit — product call:**

| Policy | Behavior | Trade-off |
|---|---|---|
| Public reopen (default) | First new requester wins | Simplest; early rejected users have often left |
| Standby waitlist | Keep first ~2×stock rejected users; offer released units in order with a short claim TTL | Most faithful to FCFS; adds offer/notification/cascade machinery |
| Deterministic close | Never reopen; leftover stock handled by manual restock | Simplest, zero flapping; undersells until someone intervenes |

If the business requires "all 100K units must sell," pick standby or the
scheduled round. If leftovers can go to the next sale, deterministic close is
fine.

## 6. Redis Failure Remediation

Framing that makes this tractable: **Redis holds a materialized view of DB
state; the DB conditional decrement is the physical no-oversell guarantee.**
`admitted` is reconstructible as
`COUNT(orders WHERE status IN (CONFIRMED, PENDING_PAYMENT, HELD))`,
`released` as `COUNT(RELEASED)`, the user set from the orders table. Every
failure mode reduces to "how long is the view stale, and which way does the
error bias?" — and every uncertainty is biased toward **undersell**, because
oversell is irreversible and undersell is a restock.

**Scenario A — primary dies, replica promotes (Sentinel/Cluster, 10–30 s
blip).** Async replication may lose recent writes; the asymmetry matters:

- *Lost `INCR`s* → counter undercounts → gate over-admits. The DB guard
  catches it (`reserved > 0` matches zero rows for the excess); those users
  get an apology/coupon instead of a phantom order. Bad press, zero physical
  oversell.
- *Lost `SADD`s* → a duplicate slips through to the DB, dies on the unique
  constraint. Safe.
- *Lost `released`* → brief undersell. Harmless.

If the blip is unacceptable, `WAIT 1 tso` after the admission script gives
near-synchronous replication for a few ms of added latency.

**Scenario B — Redis tier fully down.** Two sane policies; pick per sale:

- **Fail-closed (default for flash sales):** circuit breaker in the Purchase
  API trips within ms; API returns 503 + `Retry-After`; sale page shows
  "temporarily paused." Overselling 100K physical units forces cancellations
  and a PR incident; a 30-second pause is recoverable. The CDN page and
  gateway sale-window gate keep working, so the outage degrades to "can't buy
  right now," not "site down."
- **Degrade to the DB path:** fall back to the transactional conditional
  decrement directly in the request path (the same SQL the workers use, plus
  order insert and unique constraint). Fully correct, but requests serialize
  on one inventory row (~500–2K TPS). Survivable only if the gateway
  simultaneously clamps admission (e.g., a token bucket admitting ~1K RPS;
  everyone else gets "try again"). FCFS degrades to "first to win the row
  lock."

**Anti-pattern:** "keep the counter in app memory while Redis is down."
N stateless nodes each believing they are the counter guarantees oversell.
Single writer or nobody.

**Recovery — rebuild before reopening:**

1. Freeze admission (fail-closed already did this)
2. Rebuild counters and the user set from the orders/inventory tables
3. Bias every uncertainty toward undersell: set `admitted` rounded **up**
   (max plausible), `released` rounded **down**
4. Resume — in-flight user retries are naturally idempotent because order ids
   are deterministic on `(user_id, event_id)`: a retry either finds an
   existing order or admits cleanly, never twice

**Continuously, not just during outages:** a reconciler compares Redis
counters against DB-derived counts every second or so and alerts/heals on
drift. Same logic as recovery, running as a watchdog — which means the
recovery path is exercised every day, not just during the incident.

## 7. Data Stores & Storage Sizing

| Store | Contents | Why |
|---|---|---|
| Redis (cluster, HA) | admission counter, released counter, per-user set (TTL = sale + buffer), sale window, stock cache | Sub-ms atomic decisions |
| Kafka / SQS | admitted purchase messages | Buffer + decouple; partitions give worker throughput without breaking FCFS (already fixed at admission) |
| PostgreSQL — primary + read replicas, **partitioned by `sale_event_id`** | `orders`, `inventory`, `payments` | Durable source of truth; unique constraint = final no-oversell guard |
| CDN | sale page, images | Absorb the page-refresh stampede |

### Why not shard the orders table

The admission gate bounds writes at O(stock), and the queue smooths them, so
neither volume nor write rate justifies sharding:

- **Volume:** ≤ 100K orders/sale at ~0.5–1 KB/row → ~100 MB per event.
  Even 10 events/day → ~1 GB/day → ~365 GB/year. A single PostgreSQL primary
  on NVMe handles multi-TB tables.
- **Write rate:** ≤ 100K inserts spread over the drain → a few thousand TPS
  peak.
- **Reads:** post-sale order-status polling is cacheable (short TTL on the
  `PENDING → CONFIRMED` transition) and served by replicas.

The actual DB hot spots are the **inventory row lock** during drain (bounded
by worker concurrency) and **index/vacuum bloat** over years — neither is
solved by sharding.

The ladder before sharding:

| Step | What | What it buys |
|---|---|---|
| 1 | Single primary + read replicas | This entire design fits |
| 2 | Partition by `sale_event_id` (or time range) | Small hot B-trees per event; cheap archival (detach old partitions); fast "drop the failed event" |
| 3 | OLTP/OLAP split — stream orders to a warehouse for marketing funnels | Keeps ad-hoc analytics off the primary |
| 4 | Shard by `user_id` | Only when 1–3 are exhausted |

Two sharding costs worth naming: the unique constraint on
`(user_id, sale_event_id)` stays local only if sharded by `user_id` (but then
per-event analytics scatter-gather); sharding by `sale_event_id` pushes the
dedup guard itself cross-shard, which is far worse. Plus rebalancing,
per-shard schema changes, and backup/failover correctness — new failure modes
for zero benefit at 100 MB/event.

Shard when the **platform**, not the feature, outgrows a single primary, with
measured (not forecast) thresholds: sustained order writes beyond ~50–100K
TPS, an orders table in the tens of TB where maintenance/backup/failover
windows hurt, or multi-region data residency.

## 8. Guarantees & Failure Modes

**No oversell — three layers:** Redis atomic admission ≤ stock → DB
conditional decrement (`reserved > 0`) → DB unique constraint per user. Even
with bugs or replays, the SQL is the physical backstop.

**One unit per user — three layers:** frontend disables the button; Redis
`SADD` rejects duplicates and makes retries idempotent; DB unique constraint
as truth.

**Idempotency:** admission keyed on `(user_id, event_id)`; order id derived
deterministically so client retries never double-admit.

**Thundering herd at T0:** sale page from CDN; buy button disabled client-side
until T0 with random 0–2 s activation jitter; gateway rate limits per
user/IP; optional captcha / signed sale tokens issued pre-T0 to blunt bots.

**Monitoring:** admission latency p99, counter vs stock, queue depth and
drain rate, payment failure rate, `released` rate, Redis↔DB reconciler drift.

## 9. Requirement → Mechanism Map

| Stated requirement | Mechanism |
|---|---|
| Sale starts at a particular time | Gateway gate on sale window (server-side truth) + client button schedule |
| Requests may exceed stock | Atomic admission counter caps accepted requests at stock |
| One unit per user | Redis SADD + DB unique constraint + disabled button |
| No cart, direct buy | Single `POST /sales/{event}/orders` endpoint |
| FCFS, out of stock the moment stock exhausts | Redis Lua = serialization point; `SOLD_OUT` pub/sub flips all clients instantly |
| API processes requests in queue | Kafka + order workers, bounded at O(stock) |
| Instant "no stock" error when demand > stock | Front-door reject — never touches queue or DB |
| Success + order id returned, background processing | Enqueue-and-return-`PENDING`; workers confirm async |
| Loader stops on response; error removes product | Admission decision is ~5–20 ms; `no_stock` payload drives UI removal |

## 10. Trade-offs & Interview Notes

- **Redis gate vs pure DB row lock:** `UPDATE ... WHERE count > 0` alone is
  simpler and correct but serializes 1M requests on one row — dies well under
  the load. Keep it as the fallback path and durable guard, not the gate.
- **Instant-reject exactness:** the counter approach is *exactly* correct here
  only because one-unit-per-user makes demand countable; it does not work if
  users can buy variable quantities.
- **Strict global FCFS needs one serialization point** (the Lua script).
  Queue partitioning would break ordering — acceptable only because ordering
  was already fixed at admission.
- **Failure bias:** every uncertainty (replication loss, rebuild rounding)
  errs toward undersell; oversell is irreversible, undersell is a restock.
- **Premature sharding:** at 100 MB/event the correct answer is
  primary + replicas + partitioning; the interview credit comes from pushing
  back, naming the measured thresholds, and noting the Redis gate already did
  the hard scaling work so the DB never sees the herd.
