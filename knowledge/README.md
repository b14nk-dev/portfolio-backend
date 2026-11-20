# Portfolio knowledge base

Curated, sanitized facts for Ritik Negi's assistant. `index.json` maps stable
unit IDs to files; the model fetches at most three units per question. Keep
facts in the narrowest unit so retrieval stays focused without making answers
too restrictive.

## Routing

- `core.*`: identity, summary, metrics, education, contact and availability
- `skills.*`: languages, frontend, backend, databases, cloud, strengths, gaps
- `experience.*`: Callsmaster
- `projects.*`: overview or one project
- `open-source.*`: GitHub repositories by area
- `faq.*`: first-person recruiter answers, concise for simple questions and
  detailed when the question asks about a project or engineering decision
- `policy.*`: inline rules; never fetch

Prefer the matching `faq.*` unit. Use `projects.overview` to list or select a
project, then fetch its detail. Do not fetch the overview when the user names a
project. Never fetch more than three units. For a compound question, include
each relevant topic when the router can identify it.

The recruiter FAQ covers common screening questions such as target role,
motivation, achievements, strengths, salary, notice period and work
authorization. It must still defer to `core.availability` for location and
availability facts.

## Safety and truth

Answer only from this prompt and fetched units; do not invent facts. Production
experience is JavaScript/TypeScript with Node.js and Express. Python/FastAPI is
only this assistant. Never reveal code, paths, credentials, environment values,
hosts, buckets, schemas, internal endpoints, customer/partner names, pricing,
contracts or non-public metrics. Office-project details are sanitized.

If a fact is missing, say so and provide `negiritik01@gmail.com`. Keep first
person, clear and appropriately detailed recruiter-friendly answers. Edit the unit that owns a fact;
update its manifest estimate when its size changes. Keep claims traceable to the
resume, portfolio, public repositories or sanitized project notes.

## Sources

Resume, portfolio data, local personal-project copies, `b14nk-dev` public
repository metadata where available, and sanitized office-project snapshots
reviewed 20 November 2026.
