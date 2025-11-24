from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class BookMetadata:
    """Value object for EPub book metadata."""

    title: str | None = None
    creator: str | None = None
    description: str | None = None
    pubdate: str | None = None
    publisher: str | None = None
    identifier: str | None = None
    language: str | None = None
    rights: str | None = None
    modified_date: str | None = None
    layout: str | None = None
    orientation: str | None = None
    flow: str | None = None
    viewport: str | None = None
    spread: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format (excluding None values)."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BookMetadata":
        """Generate from dictionary."""
        # Pass only fields that exist in the dictionary to use default values correctly
        return cls(**{field: data[field] for field in cls.__dataclass_fields__ if field in data})

    @classmethod
    def from_json_string(cls, json_string: str | None) -> "BookMetadata":
        """Generate from JSON string."""
        if not json_string:
            return cls()

        import json

        try:
            data = json.loads(json_string)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            return cls()
