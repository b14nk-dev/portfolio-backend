# Open Source — Backend and Tooling

## node-and-express-server-template

<https://github.com/b14nk-dev/node-and-express-server-template> ·
JavaScript, Node.js, Express

An Express template built on two ideas: dynamic route registration and
automatic controller error handling.

- Routes are discovered from `routes/` instead of wired by hand.
- A custom `Router` wrapper records route metadata (path, method, description)
  and wraps handlers in `asyncHandler`, forwarding rejected promises to error
  middleware.
- Centralized error handling gives consistent API error responses; the route
  table is self-documenting.

Shows API design opinions: modular structure, metadata, and no repeated
`try/catch` in controllers.

## assignment-server / assignment-client

- Server: <https://apna-college-server.vercel.app> · JavaScript, Node.js,
  Express, MongoDB — REST API for a study tracker with users, topics, problems
  and progress; JWT auth middleware.
- Client: <https://apna-college-client.vercel.app> · TypeScript, Next.js,
  Tailwind CSS — login, topic lists, progress ring charts, per-topic
  accordions.

## Blind Chat

<https://github.com/b14nk-dev/Blind_Chat_Frontend> ·
<https://github.com/b14nk-dev/Blind_Chat_Backend> · Next.js, Socket.IO, Node.js

Anonymous real-time chat with bidirectional Socket.IO events and no accounts
(2023, one of the earlier projects).

The backend is a small Express and Socket.IO service while the frontend is a
Next.js application. The project is useful for explaining event-driven
communication, client/server coordination and the trade-off between anonymous
access and persistent user identity.

## portfolio-backend

<https://github.com/b14nk-dev/portfolio-backend> · Python, FastAPI, Gemini API

Backend for this AI assistant: streams newline-delimited JSON events (`status`,
`token`, `error`, `done`) from a Gemini model restricted to a curated knowledge
base. Personal project — Python/FastAPI is used only here and is not
representative of his JavaScript/TypeScript + Node.js backend stack.
