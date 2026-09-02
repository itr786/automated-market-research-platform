from dataclasses import dataclass
from typing import Callable

from django.db import transaction

from research.models import Evidence, ResearchBrief


@dataclass(frozen=True)
class ResearchResult:
    brief_id: int
    evidence_count: int
    status: str


class ResearchOrchestrator:
    """Coordinates a research run without coupling it to the HTTP request."""

    def __init__(self, progress: Callable[[int, str], None] | None = None):
        self.progress = progress or (lambda percent, message: None)

    @transaction.atomic
    def run(self, brief: ResearchBrief, sources: list[dict]) -> ResearchResult:
        if brief.status not in {ResearchBrief.Status.QUEUED, ResearchBrief.Status.FAILED}:
            raise ValueError("Brief is not ready to run")

        brief.status = ResearchBrief.Status.RUNNING
        brief.progress = 5
        brief.save(update_fields=["status", "progress", "updated_at"])
        self.progress(5, "Research started")

        created = 0
        total = max(len(sources), 1)
        for index, item in enumerate(sources, start=1):
            Evidence.objects.create(
                brief=brief,
                source=item["source"],
                quote=item["quote"],
                confidence=item.get("confidence", 0),
            )
            created += 1
            percent = min(90, 10 + int(index / total * 80))
            brief.progress = percent
            brief.save(update_fields=["progress", "updated_at"])
            self.progress(percent, f"Captured source {index} of {total}")

        brief.status = ResearchBrief.Status.COMPLETE
        brief.progress = 100
        brief.save(update_fields=["status", "progress", "updated_at"])
        self.progress(100, "Research complete")
        return ResearchResult(brief.id, created, brief.status)
