# Project — The Thai Tourism Platform (Overview)

- **Type:** Professional / office
- **Live:** <https://thethaitourism.com>
- **Stack:** Next.js 15 (App Router), React 18, TypeScript, Tailwind CSS,
  Radix UI, TanStack Query, Redux Toolkit, Express 4, Sequelize 6, PostgreSQL,
  Stripe, PayPal, AWS (S3, SES, Secrets Manager), Firebase Cloud Messaging,
  Passport OAuth, Docker, GitHub Actions

A production online travel platform for Thailand: a customer booking site plus
the internal CRM/API behind catalogue, pricing, inventory, bookings, payments,
partners and operations — two codebases, one product.

- Customer site: `projects.thai-tourism-customer`
- CRM and API: `projects.thai-tourism-api`

Talking points: two apps, one product; the money paths are the strongest part
(Stripe manual capture, PayPal, webhooks, idempotency, server-recomputed
amounts); it shows the deepest testing and migration discipline — hundreds of
tests and versioned SQL migrations with a release gate.

Never name ticketing suppliers, partners, customers, internal hosts, buckets,
endpoints, commissions or booking volumes; say "third-party
attraction/ticketing supplier API".
