from abc import ABC, abstractmethod

from src.domain.chat.entities.chat import Chat
from src.domain.chat.repositories.chat_repository import ChatRepository
from src.domain.chat.value_objects.user_id import UserId


class FindChatsByUserIdUseCase(ABC):
    @abstractmethod
    def execute(self, user_id: UserId) -> list[Chat]:
        """Retrieve all chats associated with a user ID."""


class FindChatsByUserIdUseCaseImpl(FindChatsByUserIdUseCase):
    def __init__(self, chat_repository: ChatRepository) -> None:
        self.chat_repository = chat_repository

    def execute(self, user_id: UserId) -> list[Chat]:
        """Retrieve all chats associated with a user ID."""
        return self.chat_repository.find_by_user_id(user_id)
