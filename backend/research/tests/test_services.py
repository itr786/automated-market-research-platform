from django.test import TestCase

from research.models import Market, ResearchBrief
from research.services.evidence import score_evidence
from research.services.research_runner import ResearchRunner
from research.services.review import approve, submit_for_review


class ResearchServiceTests(TestCase):
    def setUp(self):
        market = Market.objects.create(name="Energy Storage", slug="energy-storage")
        self.brief = ResearchBrief.objects.create(market=market, question="What is the market outlook?")

    def test_evidence_score_is_bounded(self):
        self.assertEqual(score_evidence(1.0, 1.0, 1.0), 1.0)
        self.assertEqual(score_evidence(4.0, -1.0, 0.5), 0.5)

    def test_runner_can_start_and_complete(self):
        runner = ResearchRunner()
        runner.start(self.brief)
        self.brief.refresh_from_db()
        self.assertEqual(self.brief.status, ResearchBrief.Status.RUNNING)
        runner.complete(self.brief)
        self.brief.refresh_from_db()
        self.assertEqual(self.brief.progress, 100)

    def test_review_transition(self):
        self.brief.status = ResearchBrief.Status.COMPLETE
        self.brief.save(update_fields=["status"])
        submit_for_review(self.brief)
        self.brief.refresh_from_db()
        self.assertEqual(self.brief.status, "review")
        approve(self.brief)
        self.brief.refresh_from_db()
        self.assertEqual(self.brief.status, "approved")
