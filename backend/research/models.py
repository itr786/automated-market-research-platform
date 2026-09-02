from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ResearchBrief(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        COMPLETE = "complete", "Complete"
        FAILED = "failed", "Failed"

    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name="briefs")
    question = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    progress = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Evidence(models.Model):
    brief = models.ForeignKey(ResearchBrief, on_delete=models.CASCADE, related_name="evidence")
    source = models.URLField()
    quote = models.TextField()
    confidence = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    captured_at = models.DateTimeField(auto_now_add=True)
