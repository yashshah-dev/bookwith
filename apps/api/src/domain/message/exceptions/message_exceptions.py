class MessageDomainException(Exception):  # noqa: N818
    """Base class for exceptions related to the Message domain."""


class MessageNotFoundException(MessageDomainException):
    def __init__(self, message_id: str) -> None:
        self.message_id = message_id
        super().__init__(f"Message with ID {message_id} not found")


class MessageAlreadyDeletedException(MessageDomainException):
    def __init__(self) -> None:
        super().__init__("This message has already been deleted")


class MessageDeliveryFailedException(MessageDomainException):
    def __init__(self) -> None:
        super().__init__("Message delivery failed")


class MessagePermissionDeniedException(MessageDomainException):
    def __init__(self) -> None:
        super().__init__("You do not have permission to access this message")
