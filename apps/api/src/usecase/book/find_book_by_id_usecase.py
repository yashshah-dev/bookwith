"""Use case for retrieving a specific book"""

from abc import ABC, abstractmethod

from src.domain.book.entities.book import Book
from src.domain.book.exceptions.book_exceptions import BookNotFoundException
from src.domain.book.repositories.book_repository import BookRepository
from src.domain.book.value_objects.book_id import BookId


class FindBookByIdUseCase(ABC):
    """FindBookByIdUseCase defines the use case interface for retrieving a specific book by ID."""

    @abstractmethod
    def execute(self, book_id: str) -> Book:
        """Retrieve a specific book by ID"""


class FindBookByIdUseCaseImpl(FindBookByIdUseCase):
    """FindBookByIdUseCaseImpl is the implementation of the use case for retrieving a specific book by ID."""

    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    def execute(self, book_id: str) -> Book:
        """Retrieve a specific book by ID. Raise exception if not found."""
        book_id_obj = BookId(book_id)
        book = self.book_repository.find_by_id(book_id_obj)

        if book is None:
            raise BookNotFoundException(book_id)

        return book
