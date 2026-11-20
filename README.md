# portfolio-backend

Backend for the "ask about Ritik" assistant on
<https://ritik-negi.vercel.app>. It answers recruiter questions from a curated
knowledge base using an LLM, and streams the answer to the browser token by
token. Answers are explanation-first — a direct answer followed by short
context or labelled bullets when useful — so they remain easy to scan without
being artificially compressed.

## Stack

- FastAPI + Uvicorn
- Google Gemini API via the official `google-genai` SDK (streaming)
- Markdown knowledge base in [`knowledge/`](knowledge/README.md)

This is a personal Python service. Ritik's production work is
JavaScript/TypeScript with Node.js and Express.

## Setup

```bash
uv sync
cp .env.example .env   # set GEMINI_API_KEY
uv run uvicorn main:app --reload
```

`GET /health` returns `{"status": "ok"}`. For a simple manual check, start the
server and open `/health` and `/api/v1/ai/warmup` in your browser. Both should
return a small JSON response.

`GET /api/v1/ai/warmup` wakes a sleeping deployment and returns
`{"status":"ready"}`. Call it when the portfolio loads and keep the AI loader
visible until it returns successfully:

```js
await fetch(`${API_URL}/api/v1/ai/warmup`, { cache: "no-store" });
```

This endpoint does not call Gemini or consume model tokens; it only confirms
that the FastAPI process is awake.

## API

`POST /api/v1/ai/`

```json
{ "question": "Do you know Java and Spring Boot?" }
```

`question` is trimmed and must be 5–500 characters. The response is
`application/x-ndjson` (one JSON object per line, no buffering).

### Stream events

| `type` | Fields | Meaning |
| --- | --- | --- |
| `status` | `stage` (`thinking`) | Progress indicator |
| `token` | `text` | Append to the answer |
| `followups` | `items` (array of strings) | Suggested next questions; render as clickable chips |
| `links` | `items` (array of `{label, url}`) | Validated links related to the answer |
| `rate_limit` | `retry_after` | Gemini's wait time in seconds, when it reported one |
| `error` | `message` | User-safe error; stop rendering |
| `done` | — | End of stream |

Order is always `status` … `token`* [`followups`] [`links`] [`rate_limit`]
`done`. `rate_limit` is also emitted before `error` when a limit is hit.

Example:

```
{"type": "status", "stage": "thinking"}
{"type": "token", "text": "No — Java and Spring Boot aren't part of my stack. "}
{"type": "token", "text": "My primary backend is JavaScript/TypeScript with Node.js and Express."}
{"type": "followups", "items": ["What is your primary stack?", "Do you know Python?"]}
{"type": "links", "items": [{"label": "Resume", "url": "https://github.com/b14nk-dev/b14nk-dev/raw/main/assets/Ritik_Negi_SDE_2_Resume.pdf"}]}
{"type": "done"}
```

### Extras contract

The model is asked to append one machine-readable block after the answer:

```
<extras>{"followups": ["..."], "links": [{"label": "...", "url": "..."}]}</extras>
```

The server strips this block from the token stream, validates it, and emits it
as the `followups` and `links` events. The raw tags never reach the client.

- `followups`: up to 4, deduplicated, 140 characters max.
- `links`: up to 3. Only URLs that already exist in the knowledge base are
  accepted (plus `mailto:negiritik01@gmail.com`); anything else is dropped.
- Malformed JSON, an unterminated block, or a block split across chunks is
  handled safely — the answer still streams, extras are simply omitted.

Clients should still validate URLs before rendering, and prefer the structured
`links` event over scraping markdown from the answer.

## Rate limits

Gemini free quotas apply per project and per model. Before each request the
backend checks that model's RPM window (`llm/pace.py`) and waits for a free slot.
If the window stays full for more than 10 s the request is treated as
rate-limited instead of stalling the stream. On a 429 it still reads Gemini's `RetryInfo` (or the `Retry-After`
header), moves to the next model in the pool, and only emits an `error` event
when every model is exhausted.

- Daily-quota 429s (`...PerDay...` in the quota id) mark that model unusable for
  the rest of the request.
- When every model is momentarily limited, the backend waits once for the
  shortest advertised delay (capped at 30 seconds), then makes one more pass.
- If Gemini reported a wait time, it is emitted before the error:

```json
{ "type": "rate_limit", "retry_after": 27 }
```

### Model fallback

The default order in `llm/gemini_models.py` follows the limits free projects
report in AI Studio (late 2026):

| Model | Free RPM | Free RPD | Role |
| --- | --- | --- | --- |
| `gemini-3.5-flash-lite` | 15 | 500 | primary; balanced and highest headroom |
| `gemini-3.1-flash-lite` | 15 | 500 | second Flash-Lite (shuts down May 2027) |
| `gemini-3.8-flash` | 5 | 20 | newest Flash; best answers, tiny quota |
| `gemini-3.6-flash` | 5 | 20 | previous Flash |
| `gemma-4-31b-it` | 30 | 14,400 | last resort at traffic spikes |

Flash-Lite leads because Flash's 20 RPD is shared by the whole project, so one
busy day would exhaust it as the primary. `GEMINI_MODELS` overrides the order
with a comma-separated list. Google publishes no per-model free numbers and
does not guarantee them; AI Studio's rate-limit page is authoritative. Answers
stream through `client.models.generate_content_stream`, with the SDK's own
retries disabled (`attempts=1`) so the pool and pacer stay in charge.

### Client limits

To stop one visitor spending the shared Gemini quota, the chat endpoint uses
[SlowAPI](https://slowapi.readthedocs.io/) with a per-IP key before streaming
starts. Each client gets 10 questions per day by default:

```text
CLIENT_RATE_LIMIT=10     # count, or a rate such as 10/day; 0 disables
CLIENT_RATE_WINDOW=86400 # window length in seconds when using a count
```

The key prefers `X-Forwarded-For` and `X-Real-IP`, so it works behind the
deployment proxy. A rejected request returns HTTP `429` with a JSON `detail`,
`Retry-After`, and SlowAPI's `X-RateLimit-*` headers, before any NDJSON is
written. The window is in-process, so each worker enforces its own copy; a
shared store would be needed for a hard multi-instance quota.

## Knowledge base

`knowledge/index.json` lists the units (`core.*`, `skills.*`, `experience.*`,
`projects.*`, `open-source.*`, `faq.*`, `policy.*`). `llm/router.py` maps a
question's keywords to units, which `services/prompting.py` prefetches and
injects as reference facts — the model calls no tools. Policy units are inlined
into the system prompt. Sensitive information rules live in
[`knowledge/README.md`](knowledge/README.md).

The base is loaded once at import time, so restart the server after editing it.
