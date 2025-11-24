from dataclasses import dataclass


@dataclass(frozen=True)
class BookTitle:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Title is required")
        if len(self.value) > 100:
            raise ValueError("Title must be 100 characters or less")
