from rest_framework import viewsets
from .models import Evidence, Market, ResearchBrief
from .serializers import EvidenceSerializer, MarketSerializer, ResearchBriefSerializer


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.order_by("name")
    serializer_class = MarketSerializer
    lookup_field = "slug"


class ResearchBriefViewSet(viewsets.ModelViewSet):
    queryset = ResearchBrief.objects.select_related("market").prefetch_related("evidence").order_by("-created_at")
    serializer_class = ResearchBriefSerializer
    filterset_fields = ("status", "market")


class EvidenceViewSet(viewsets.ModelViewSet):
    queryset = Evidence.objects.order_by("-captured_at")
    serializer_class = EvidenceSerializer
