from django.urls import include, path
from rest_framework.routers import DefaultRouter
from research.views import EvidenceViewSet, MarketViewSet, ResearchBriefViewSet

router = DefaultRouter()
router.register("markets", MarketViewSet)
router.register("research", ResearchBriefViewSet)
router.register("evidence", EvidenceViewSet)

urlpatterns = [path("api/", include(router.urls))]
