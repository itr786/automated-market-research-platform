# Architecture

## Request path

The Next.js client uses REST for durable resources and WebSockets for transient progress events. A research brief is persisted before execution begins, so reconnecting clients can recover the current state.

## Research pipeline

```text
Brief
  ↓
Quota check
  ↓
Source registry
  ↓
Research orchestration
  ↓
Evidence capture
  ↓
Evidence scoring
  ↓
Report composition
  ↓
Review queue
  ↓
Approval / changes requested
```

## Design decisions

- **Persist state:** browser connectivity must not determine whether a research run exists.
- **Separate evidence:** source URL, quote, confidence, and capture time remain traceable independently of report prose.
- **Explicit transitions:** review actions validate the current state before changing it.
- **Typed realtime events:** frontend WebSocket handling uses a small event contract rather than untyped component state.
- **Service boundaries:** orchestration, quota, segmentation, evidence, and report composition are independently testable.

## Scaling direction

For a larger deployment, the orchestration entry point can move behind a task queue while PostgreSQL remains the source of truth for job state. A channel layer can fan progress events across multiple ASGI workers. The portfolio implementation keeps those boundaries visible without requiring a cloud-specific dependency.
