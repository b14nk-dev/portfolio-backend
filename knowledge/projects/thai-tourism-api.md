# Project — Thai Tourism CRM and API

Large Express/PostgreSQL service: ~72 route modules, 73 controllers, 114
Sequelize models, 130 SQL migrations and 600+ tests.

- **Domains:** catalogue, pricing, inventory, bookings, carts, checkout,
  fulfillment, vouchers, cancellations, refunds, payments, partners, agents,
  operations, content and notifications.
- **Payments:** Stripe manual capture, PayPal, webhooks, reconciliation and
  idempotency; server-side pricing and internal-field redaction.
- **Auth/security:** JWT httpOnly cookies, Passport OAuth (Google, Facebook,
  Apple, Twitter, LINE, Kakao), principal checks, CSRF, rate limits,
  correlation IDs, audit logs and Helmet.
- **Delivery:** SQL-first migrations with release gate (no `sequelize.sync`),
  structured logs, S3 media, scheduled jobs, Docker, GitHub Actions and
  `node:test`/Vitest/Playwright.

The API is organized around business domains rather than one large booking
handler. Important engineering concerns include durable background work for
external booking messages, replay-safe webhook processing, idempotency for
retryable operations, permission checks that remain fresh, catalogue and
media-integrity checks, and bounded operational scripts. These are described at
a system-design level only; private integration details are intentionally not
part of the knowledge base.

Never name suppliers, partners, customers, hosts, buckets, endpoints,
commissions or booking volumes.
