from dataclasses import dataclass
from enum import Enum


class AnnotationTypeEnum(Enum):
    HIGHLIGHT = "highlight"


@dataclass(frozen=True)
class AnnotationType:
    value: str

    def __post_init__(self) -> None:
        if not any(self.value == type_.value for type_ in AnnotationTypeEnum):
            raise ValueError(f"Invalid annotation type: {self.value}")

    @classmethod
    def highlight(cls) -> "AnnotationType":
        """Create a highlight type annotation"""
        return cls(AnnotationTypeEnum.HIGHLIGHT.value)

    @classmethod
    def default(cls) -> "AnnotationType":
        """Create a default type annotation"""
        return cls.highlight()

    @classmethod
    def from_string(cls, type_str: str | None) -> "AnnotationType":
        """Generate AnnotationType from string"""
        if not type_str:
            return cls.default()
        return cls(type_str)
