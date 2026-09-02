from rest_framework import serializers
from .models import Evidence, Market, ResearchBrief


class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = "id", "source", "quote", "confidence", "captured_at"


class ResearchBriefSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(source="market.name", read_only=True)
    evidence = EvidenceSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchBrief
        fields = "id", "market", "market_name", "question", "status", "progress", "evidence", "created_at", "updated_at"


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = "id", "name", "slug", "created_at"
