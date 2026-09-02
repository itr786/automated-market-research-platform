from django.db import transaction

from research.models import ResearchBrief


ALLOWED_TRANSITIONS = {
    ResearchBrief.Status.COMPLETE: {"review"},
    "review": {"approved", "changes_requested"},
    "changes_requested": {"review"},
}


@transaction.atomic
def submit_for_review(brief: ResearchBrief) -> ResearchBrief:
    if brief.status != ResearchBrief.Status.COMPLETE:
        raise ValueError("Only completed research can be submitted for review")
    brief.status = "review"
    brief.save(update_fields=["status", "updated_at"])
    return brief


@transaction.atomic
def approve(brief: ResearchBrief) -> ResearchBrief:
    if brief.status != "review":
        raise ValueError("Only research in review can be approved")
    brief.status = "approved"
    brief.save(update_fields=["status", "updated_at"])
    return brief
