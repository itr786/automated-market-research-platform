from django.core.exceptions import PermissionDenied


class QuotaService:
    """Keeps usage checks in one place so API and background jobs share rules."""

    def __init__(self, limit: int):
        self.limit = limit

    def ensure_available(self, used: int, requested: int = 1) -> None:
        if used + requested > self.limit:
            raise PermissionDenied("Research quota exceeded")

    def remaining(self, used: int) -> int:
        return max(0, self.limit - used)
