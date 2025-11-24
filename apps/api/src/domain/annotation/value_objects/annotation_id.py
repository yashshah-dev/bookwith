import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class AnnotationId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            object.__setattr__(self, "value", str(uuid.uuid4()))
        elif not isinstance(self.value, str):
            raise ValueError("AnnotationId must be a string")

    @classmethod
    def new(cls) -> "AnnotationId":
        """Generate a new ID"""
        return cls(str(uuid.uuid4()))

    @classmethod
    def from_string(cls, id_str: str | None) -> "AnnotationId":
        """Generate AnnotationId from string"""
        if not id_str:
            return cls.new()
        return cls(id_str)
