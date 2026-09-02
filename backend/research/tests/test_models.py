from django.test import TestCase
from research.models import Market, ResearchBrief


class ResearchBriefTests(TestCase):
    def test_new_brief_starts_queued(self):
        market = Market.objects.create(name="Cloud Security", slug="cloud-security")
        brief = ResearchBrief.objects.create(market=market, question="What is the market outlook?")
        self.assertEqual(brief.status, ResearchBrief.Status.QUEUED)
        self.assertEqual(brief.progress, 0)
