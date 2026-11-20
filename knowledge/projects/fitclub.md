# Project — Fitclub Gym CRM

- **Type:** Professional office work, Jul 2024–Feb 2026
- **Live:** <https://fitclub.coupontodeal.com>
- **Stack:** Node/Express, PostgreSQL/Sequelize, React/Vite, Redux Toolkit,
  TanStack Query, Ant Design, Tailwind, JWT, S3, Razorpay

Gym-business CRM/back office with ~10,000 member records: memberships,
attendance, billing, staff/classes, inventory, leads, branches, reports,
imports, roles/permissions and audit history. Snapshot scale: ~68 models, 65
route modules, 150 pages and 250 components.

Highlights: JWT/RBAC, Razorpay/GST invoicing/credit notes, S3 uploads, QR codes,
scheduled jobs, transactional email, CI/CD and PostgreSQL tuning for a 35%+
dashboard gain.

The system is split between an Express API and a React/Vite dashboard. The API
organizes business areas into route, controller, service and model layers,
while the dashboard provides role-aware screens for members, branches,
attendance, packages, staff, classes, inventory, invoices, reports and imports.
This is a good example of operational software where permissions, auditability
and data consistency matter as much as the UI.
