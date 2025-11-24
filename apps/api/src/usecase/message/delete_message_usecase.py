"""Message deletion use case"""

from abc import ABC, abstractmethod

from src.domain.message.exceptions.message_exceptions import MessageNotFoundException
from src.domain.message.repositories.message_repository import MessageRepository
from src.domain.message.value_objects.message_id import MessageId


class DeleteMessageUseCase(ABC):
    @abstractmethod
    def execute(self, message_id: str) -> None:
        """Delete a message"""

    @abstractmethod
    def execute_bulk(self, message_ids: list[str]) -> list[str]:
        """Bulk delete multiple messages. Return list of message IDs that failed to delete"""


class DeleteMessageUseCaseImpl(DeleteMessageUseCase):
    def __init__(self, message_repository: MessageRepository) -> None:
        self.message_repository = message_repository

    def execute(self, message_id: str) -> None:
        """Delete a message. Actually performs logical deletion"""
        message_id_obj = MessageId(message_id)
        message = self.message_repository.find_by_id(message_id_obj)

        if message is None:
            raise MessageNotFoundException(message_id)

        message.mark_as_deleted()

        self.message_repository.save(message)

    def execute_bulk(self, message_ids: list[str]) -> list[str]:
        """Bulk delete multiple messages. Return list of message IDs that failed to delete"""
        message_id_objects = [MessageId(id_str) for id_str in message_ids]

        failed_ids = self.message_repository.bulk_delete(message_id_objects)

        return [failed_id.value for failed_id in failed_ids]
