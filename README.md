# BQBYTE AI Gateway 🚀

A production-shaped **FastAPI gateway** that sits in front of a [Flowise](https://flowiseai.com/) Cloud–hosted RAG pipeline, exposing it as a clean, typed, observable REST API. Built as the AI-serving layer for BQBYTE's supply chain intelligence use case — supplier performance, SLA compliance, procurement policy, and risk analysis — over a 432-chunk indexed knowledge base.

This is a **backend-only service** — it's meant to be consumed by other applications over HTTP, not accessed directly by end users.

---

## 🚀 Live Deployment

> BQBYTE AI Gateway is containerized with Docker and deployed on Render.

| Resource | URL |
|---|---|
| 🌐 **API** | https://bqbyte-ai-gateway.onrender.com |
| 📚 **Swagger UI** | https://bqbyte-ai-gateway.onrender.com/docs |
| ❤️ **Health Check** | https://bqbyte-ai-gateway.onrender.com/health |
| 🔍 **Readiness Check** | https://bqbyte-ai-gateway.onrender.com/ready |

## What it does

The gateway itself does not run any model. Its job is to be the production front door for one:

- Validates and shapes incoming requests before they ever reach the LLM
- Forwards queries to a Flowise-hosted RAG chain (LLM + Gemini embeddings + vector retrieval)
- Translates upstream failures (timeouts, connection errors, bad responses) into correct, distinguishable HTTP status codes
- Logs every request with a correlation ID and latency
- Exposes liveness and readiness endpoints for orchestration/monitoring
- Ships as a Docker image, built and pushed automatically via CI on every merge to `main`

---

## Architecture

```
app/
├── main.py                    # FastAPI app factory — wires routers, middleware, exception handlers
├── routes/
│   ├── health.py               # GET /health (liveness), GET /ready (readiness — pings Flowise)
│   └── predict.py              # POST /predict — the inference endpoint
├── services/
│   └── flowise_service.py      # Only place that talks to Flowise (httpx async client)
├── models/
│   ├── request.py              # PredictionReq — typed, validated request schema
│   └── response.py             # PredictionRes — typed response schema
├── middlewares/
│   └── logging.py              # Per-request UUID + latency logging, X-Request-ID header
├── exceptions/
│   ├── flowise_exception.py    # Domain exception hierarchy (Timeout / Connection / Response)
│   ├── translator.py           # Maps httpx exceptions → domain exceptions
│   └── handlers.py             # Maps domain exceptions → HTTP status codes + JSON error body
└── utils/
    ├── config.py                # pydantic-settings — env-driven configuration
    ├── exception_handler.py     # Legacy/alternate handler implementation (superseded by exceptions/handlers.py — not wired into main.py, kept for reference)
    └── logger.py                # Shared structured logger

tests/
├── conftest.py                  # Shared TestClient fixture
├── test_root.py                 # GET / — welcome message
├── test_health.py               # GET /health — liveness check
└── test_predict.py              # POST /predict — service layer mocked
.github/workflows/ci.yml        # Test → build → push Docker image
Dockerfile
requirements.txt
```

**Design principle:** routes stay thin, all external I/O is isolated in the service layer, and cross-cutting concerns (config, logging, exceptions) are pulled out rather than scattered through the routes.

---

## API Reference

### `POST /predict`

Send a query to the RAG pipeline and get back a generated answer.

**Request**
```json
{
  "query": "What is our current SLA compliance rate with Supplier X?"
}
```
`query` is required, 1–500 characters.

**Response**
```json
{
  "success": true,
  "res": "Supplier X is currently at 94.2% SLA compliance over the last quarter..."
}
```

**Error responses**

| Status | Meaning |
|---|---|
| `422` | Invalid request body (fails Pydantic validation) |
| `502` | Flowise returned an unsuccessful HTTP response |
| `503` | Could not connect to Flowise |
| `504` | Flowise request timed out (30s timeout) |
| `500` | Unhandled internal error |

### `GET /health`

Liveness check — confirms the process is up. Does not call out to Flowise.

```json
{ "status": "healthy", "service": "BQBYTE AI Gateway", "version": "1.0.0" }
```

### `GET /ready`

Readiness check — pings the Flowise health URL (5s timeout) and reports whether the upstream is reachable. Returns `503` if not.

```json
{ "status": "ready", "service": "BQBYTE AI Gateway" }
```

### `GET /`

```json
{ "message": "Welcome to BQBYTE AI Gateway 🚀" }
```

Interactive API documentation is available through [Swagger UI](https://bqbyte-ai-gateway.onrender.com/docs) on the deployed instance, or at `/docs` when running locally.

---

## Getting Started

### Prerequisites
- Python 3.12+
- A running Flowise instance (cloud or self-hosted) with a prediction endpoint

### Local setup

```bash
git clone https://github.com/Theghost1008/bqbyte-ai-gateway.git
cd bqbyte-ai-gateway

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
FLOWISE_API_URL=https://your-flowise-instance/api/v1/prediction/<chatflow-id>
FLOWISE_HEALTH_URL=https://your-flowise-instance/api/v1/ping
```

Run the service:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for the interactive API explorer.

### Running tests

```bash
pytest -v
```

Covers the root, health, and predict endpoints. The predict test mocks the service layer (not the HTTP call), so the suite runs without a live Flowise instance.

### Docker

```bash
docker build -t bqbyte-ai-gateway .
docker run -p 8000:8000 --env-file .env bqbyte-ai-gateway
```

The container reads `PORT` from the environment (defaults to `8000`) and runs via `uvicorn app.main:app`.

---

## CI/CD

Every push or pull request to `main` triggers the pipeline in `.github/workflows/ci.yml`:

1. Checkout + set up Python 3.12 (with pip caching keyed on `requirements.txt`)
2. Install dependencies
3. Run `pytest -v` (using secrets-injected `FLOWISE_API_URL` / `FLOWISE_HEALTH_URL`)
4. On pushes to `main` only: build the Docker image with Buildx and push to Docker Hub, tagged both by commit SHA and `latest`, using GitHub Actions layer caching

Tests gate the build — a failing test suite means no image is built or pushed. Docker Hub credentials are only used on `main` pushes, not on pull requests, so forked PRs can't access the secrets.

---

## Configuration

All configuration is environment-driven via `pydantic-settings` (`app/utils/config.py`) — no secrets are hardcoded.

| Variable | Required | Description |
|---|---|---|
| `FLOWISE_API_URL` | Yes | Full URL of the Flowise prediction endpoint |
| `FLOWISE_HEALTH_URL` | Yes | URL used by `/ready` to check upstream health |
| `APP_NAME` | No | Defaults to `BQBYTE AI Gateway` |
| `VERSION` | No | Defaults to `1.0.0` |

---

## Roadmap

- [ ] Authentication (API key or JWT) on `/predict`
- [ ] Rate limiting
- [ ] Kubernetes manifests (Deployment/Service/HPA) wired to the existing `/health` and `/ready` probes
- [ ] Structured metrics export (Prometheus) for request latency and error rates
- [ ] Retry/backoff policy for transient Flowise failures

---

## Tech Stack

FastAPI · httpx · Pydantic / pydantic-settings · pytest · Docker · GitHub Actions · Flowise (RAG orchestration) · Gemini Embeddings