# Automated Market Research Platform

A full-stack market intelligence workspace that turns a research question into a structured, evidence-backed report workflow. The project is intentionally designed as a mid-sized engineering portfolio application rather than a CRUD demo.

## Product flow

```text
Create research brief
        ↓
Select market + target segments
        ↓
Check quota + initialize job
        ↓
Run source collection
        ↓
Capture and score evidence
        ↓
Stream live progress to dashboard
        ↓
Compose structured report
        ↓
Submit for human review
        ↓
Approve or request changes
```

## What is implemented

### Research workspace
- Market and research-brief domain model
- Queued/running/completed/failed lifecycle
- Target-segment normalization
- Source registry for different research channels
- PostgreSQL-ready persistence

### Research execution
- Service-oriented orchestration layer
- Progress callbacks for realtime delivery
- Evidence capture with confidence scoring
- Quota enforcement before execution
- Report outline/composition service
- Explicit boundaries between HTTP, orchestration, and domain logic

### Realtime UX
- Django ASGI/WebSocket endpoint
- Typed browser WebSocket client
- Live progress component
- Connection/reconnect state
- Persisted job state so a reconnecting browser can recover instead of restarting work

### Review and governance
- Submit-for-review transition
- Approval workflow
- Changes-requested state
- Review logic isolated from API serializers
- Evidence remains attached to the research brief for traceability

### Engineering quality
- Unit/service tests
- Django project checks in CI
- Docker-ready backend
- Local PostgreSQL compose stack
- Architecture documentation
- Clear service boundaries designed for future background workers

## Architecture

```text
┌───────────────────────┐
│ Next.js / React       │
│ Research Dashboard    │
└──────────┬────────────┘
           │ REST + WebSocket
           ▼
┌───────────────────────┐
│ Django REST / ASGI    │
├───────────────────────┤
│ Research API          │
│ WebSocket Consumer    │
└──────────┬────────────┘
           ▼
┌─────────────────────────────────────────┐
│ Domain Services                         │
│ Orchestrator · Quota · Evidence         │
│ Segmentation · Sources · Report · Review│
└──────────────────┬──────────────────────┘
                   ▼
             ┌────────────┐
             │ PostgreSQL │
             └────────────┘
```

See [`docs/architecture.md`](docs/architecture.md) for the detailed design and scaling direction.

## Repository structure

```text
backend/
├── config/
├── research/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── consumers.py
│   ├── services/
│   │   ├── orchestrator.py
│   │   ├── evidence.py
│   │   ├── quota.py
│   │   ├── report_builder.py
│   │   ├── review.py
│   │   ├── segmentation.py
│   │   └── source_registry.py
│   └── tests/
└── Dockerfile

frontend/
├── app/
├── components/
│   └── research-progress.tsx
└── lib/
    └── research-stream.ts

docs/
└── architecture.md
```

## Example research event

```json
{
  "status": "running",
  "progress": 64,
  "message": "Captured source 8 of 12"
}
```

The UI consumes these events independently of the persisted brief state, which keeps long-running work resilient to browser reconnects.

## Stack

- Python 3.12
- Django + Django REST Framework
- PostgreSQL
- Django Channels / ASGI
- Next.js + React + TypeScript
- WebSockets
- Pytest / Django TestCase
- Docker / GitHub Actions

## Local development

```bash
git clone <repository-url>
cd automated-market-research-platform

# Start PostgreSQL
 docker compose -f docker-compose.portfolio.yml up -d db

# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Start the Next.js application from `frontend/` and point `NEXT_PUBLIC_WS_URL` at the backend WebSocket endpoint.

## Portfolio note

This is an original portfolio/demo implementation inspired by common market-research product patterns. It contains no proprietary employer code, credentials, customer data, or private research datasets.
