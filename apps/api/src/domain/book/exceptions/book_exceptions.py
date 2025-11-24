class BookDomainException(Exception):  # noqa: N818
    """Base exception class for Book domain"""


class BookNotFoundException(BookDomainException):
    """Exception when requested book is not found"""

    def __init__(self, book_id: str) -> None:
        self.book_id = book_id
        super().__init__(f"Book with ID {book_id} not found")


class BookAlreadyStartedException(BookDomainException):
    """Exception when trying to start a book that is already started"""

    def __init__(self) -> None:
        super().__init__("This book has already been started")


class BookAlreadyCompletedException(BookDomainException):
    """Exception when trying to perform operations on a completed book"""

    def __init__(self) -> None:
        super().__init__("This book has already been completed")


class BookPermissionDeniedException(BookDomainException):
    """Exception when user does not have access permission to the book"""

    def __init__(self) -> None:
        super().__init__("You do not have permission to access this book")


class BookFileNotFoundException(BookDomainException):
    """Exception when book file is not found"""

    def __init__(self) -> None:
        super().__init__("File for this book was not found")
