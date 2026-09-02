# Automated Market Research Platform

A full-stack portfolio project for turning a market question into a traceable research workspace. It combines a Django REST API, PostgreSQL-ready domain model, asynchronous research orchestration, evidence tracking, review workflow, and a Next.js dashboard with live progress updates.

## Why this project

The goal is to demonstrate more than CRUD: long-running jobs, real-time state, evidence provenance, workflow transitions, and a frontend that can consume incremental progress without blocking navigation.

## Core capabilities

- Research brief creation with market, question, and target-segment metadata
- Research job lifecycle: queued → running → complete/failed/cancelled
- Source/evidence records with confidence and captured timestamps
- Progress events delivered over WebSockets
- Evidence-aware report sections and source traceability
- Reviewer workflow with submit-for-review and approval states
- Quota-aware research execution
- REST endpoints designed for pagination and filtering
- PostgreSQL-ready configuration with clean domain boundaries

## Architecture

```text
Next.js dashboard
      │
      ├── REST ───────────────┐
      │                       ▼
      └── WebSocket ──► Django API / ASGI
                              │
                    ┌─────────┴─────────┐
                    │ Research service  │
                    │ Evidence service  │
                    │ Review workflow   │
                    └─────────┬─────────┘
                              │
                         PostgreSQL
```

## Project structure

```text
backend/
  config/                 Django + ASGI configuration
  research/
    models.py             domain entities
    serializers.py        API contracts
    views.py              REST endpoints
    consumers.py          WebSocket progress consumer
    services/             orchestration and business rules
    tests/                model/service coverage
frontend/
  app/                    Next.js application
  components/             dashboard/report UI
  lib/                    API and WebSocket clients
```

## Engineering highlights

### Long-running research
Research execution is represented as a stateful job instead of tying the request lifecycle to the browser. This makes cancellation, retries, progress reporting, and reconnects explicit concerns.

### Evidence provenance
Evidence is modeled separately from report content so a report can show where a claim came from and how confident the system is in that source.

### Realtime updates
The ASGI layer exposes a WebSocket channel for progress events. Clients can reconnect without losing the persisted research state.

### Review workflow
Research can move through a controlled review lifecycle rather than treating generated content as immediately final.

## Stack

- Python 3.12
- Django + Django REST Framework
- PostgreSQL
- Django Channels / ASGI
- Next.js + React + TypeScript
- WebSockets
- Pytest/Django TestCase

## Running locally

```bash
cd backend
python manage.py migrate
python manage.py runserver
```

Then start the frontend with the package manager of your choice from `frontend/`.

## Portfolio note

This is an original portfolio/demo implementation inspired by common market-research product patterns. It contains no proprietary employer code, credentials, customer data, or private research datasets.
