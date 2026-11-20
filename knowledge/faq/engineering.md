# FAQ — Engineering

**Hardest problem?** Payment flows: PayU, Razorpay, Stripe and PayPal with
webhooks, idempotency and retry-safe orchestration; Callsmaster handles ~1,500
transactions/month and travel handles bookings, refunds and manual capture.

**Performance?** Cut Callsmaster dashboard/page latency 30–40% and Fitclub/Rishtey
loads 35%+ using SSR, indexing, query tuning, lazy loading, code splitting and
caching.

**Authentication?** JWT/RBAC and reusable permission middleware; travel uses
httpOnly-cookie sessions, OAuth (Google, Facebook, Apple, Twitter, LINE, Kakao)
and customer/agent/staff separation; Rishtey uses NextAuth, JWT, OTP and reset.

**Payments?** PayU, Razorpay, Stripe manual capture and PayPal checkout;
subscriptions, one-time payments, webhooks and server-side amount recomputation.

**Security?** httpOnly JWT cookies, RBAC, CSRF, rate limiting, idempotency,
audit logs, Helmet, structured logging and redacted internal cost fields.

**Testing?** Unit, integration and end-to-end tests with `node:test`, Vitest and
Playwright; travel has 600+ tests running in CI.

**Migrations?** Versioned SQL files, release gate, runner and status checks;
Sequelize associations and transactions, never ORM auto-sync in production.
