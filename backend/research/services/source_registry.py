from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDefinition:
    key: str
    label: str
    category: str
    enabled: bool = True


DEFAULT_SOURCES = (
    SourceDefinition("web", "Web research", "web"),
    SourceDefinition("news", "News and events", "news"),
    SourceDefinition("government", "Government datasets", "public-data"),
    SourceDefinition("company", "Company disclosures", "company"),
)


def enabled_sources(sources=DEFAULT_SOURCES) -> list[SourceDefinition]:
    return [source for source in sources if source.enabled]
