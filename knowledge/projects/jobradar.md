# Project — JobRadar

- **Type:** Personal
- **Stack:** Rust, Axum, Tokio, SQLite, HTMX, JavaScript browser helper

JobRadar is a local job-discovery and tracking dashboard for JavaScript and
TypeScript full-stack/backend roles in Delhi NCR and remote locations. It
collects public job listings, filters them against a profile, stores them in
SQLite and presents them in a local HTMX dashboard.

- **Collection:** independent scrapers for several public job boards, with
  request delays and robots-policy checks where applicable.
- **Browser fallback:** a small Node browser helper handles sources that need a
  rendered page; the Rust application parses and normalizes the results.
- **Workflow:** jobs move through `pending`, `applied`, `skipped` and `banned`
  states instead of being automatically applied to.
- **Matching:** title, location, skills, salary and profile rules help rank and
  filter postings.
- **Product features:** live dashboard updates, salary parsing, pruning,
  notifications, referral matching and follow-up tracking.
- **Engineering focus:** concurrency, bounded browser work, SQLite persistence,
  source-specific parsing, testable ranking and respectful request pacing.

This is a personal discovery and tracking tool. It does not submit job
applications automatically.
