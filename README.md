# Automated Market Research Platform

A production-style portfolio application for turning a research brief into a structured, evidence-backed market report. The project demonstrates asynchronous workflows, source/evidence handling, live progress streaming, report generation, and a modern Next.js research workspace.

## What it demonstrates

- Multi-step research workflow: brief → discovery → evidence → synthesis → report
- Django REST API with domain-focused applications
- PostgreSQL-ready relational data model
- WebSocket progress streaming for long-running research jobs
- Evidence records with source URL, quote, confidence, and capture time
- Research status lifecycle with failure handling
- Dashboard and research workspace built with Next.js + TypeScript
- Service-layer structure suitable for background workers and external research providers
- Automated tests around domain rules and API behavior

## Architecture

```text
Next.js Research Workspace
        │
        ├── REST API ───────────────┐
        │                           │
        └── WebSocket progress      ▼
                              Django REST API
                                    │
                         ┌──────────┼──────────┐
                         ▼          ▼          ▼
                     Research    Evidence    Reports
                         │          │          │
                         └──────────┼──────────┘
                                    ▼
                               PostgreSQL
```

## Core workflow

1. Create a market and research brief.
2. Queue the research job and expose its status through the API.
3. Stream progress events to the browser over WebSockets.
4. Store source-backed evidence against the brief.
5. Move the brief through queued, running, complete, or failed states.
6. Present the resulting research in the frontend workspace.

## Project structure

```text
backend/
  config/                 Django project configuration
  research/               domain models, API, websocket consumer, tests
frontend/
  app/                    Next.js research workspace
```

## Engineering focus

The repository is intentionally structured like a mid-sized application rather than a single CRUD example. The emphasis is on clear domain boundaries, realtime UX, persistence, and code that can evolve toward task queues and external research providers.

## Stack

Python · Django · Django REST Framework · PostgreSQL · Next.js · React · TypeScript · WebSockets

## Portfolio note

This is an original portfolio/demo implementation. It contains generated/sample data and no proprietary employer code or customer information.
