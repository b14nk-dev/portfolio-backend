# Project — JustMyFare Flight Booking Platform

- **Type:** Personal
- **Stack:** Next.js, React, TypeScript, Node.js, Express, PostgreSQL,
  Sequelize, JWT, Zod, AWS RDS, Nodemailer

JustMyFare is a flight-booking platform built as separate customer, CRM and
backend applications, plus a repeatable database bootstrap utility.

- **Customer site:** flight search, booking flow, passenger details, seat and
  ancillary selections, currency handling and booking history.
- **CRM:** staff-facing flight and booking management, PNR details, passenger
  information, permissions and operational notes.
- **Backend:** modular Express services for authentication, airports, flight
  search, bookings, passengers, payments-related details, currencies, mail and
  role/permission management.
- **Data and setup:** Sequelize models, PostgreSQL migrations and an idempotent
  bootstrap command that creates a fresh database, seeds permissions and loads
  airport reference data.
- **Security and reliability:** schema validation, JWT authentication,
  httpOnly-cookie helpers, CSRF protection, rate limiting and verification
  checks for database setup.

The project demonstrates splitting a product into user-facing, operational
and API concerns while keeping the database setup repeatable.
