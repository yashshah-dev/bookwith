import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class BookId:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("BookId is required")

        if not self._is_valid_uuid(self.value):
            raise ValueError("BookId must be a valid UUID format")

    @staticmethod
    def _is_valid_uuid(val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    @classmethod
    def generate(cls) -> "BookId":
        return cls(str(uuid.uuid4()))
