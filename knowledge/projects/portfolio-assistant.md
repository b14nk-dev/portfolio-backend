# Project — This Portfolio Assistant

- **Type:** Personal
- **Repo:** <https://github.com/b14nk-dev/portfolio-backend>
- **Stack:** Python, FastAPI, Google Gemini API, streaming JSONL

The backend for this site's assistant: it answers recruiter questions from a
curated knowledge base. A keyword router prefetches the relevant notes and a
Gemini model answers from them, streaming newline-delimited JSON so answers
appear token by token. The key constraint is
grounding — the model may answer only from the knowledge base, not its own
memory.

**Not representative of the primary stack:** personal Python/FastAPI project.
Production work is JavaScript/TypeScript with Node.js and Express. Never use it
to describe his main backend experience.
