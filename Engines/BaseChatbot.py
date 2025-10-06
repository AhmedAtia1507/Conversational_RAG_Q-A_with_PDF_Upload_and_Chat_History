from abc import ABC, abstractmethod
from typing import Iterator

class BaseChatbot(ABC):
    """
    Abstract base class for chatbots.
    Defines the interface for chatbot implementations, including methods for answering user input and retrieving chat history.
    Methods
    -------
    answer(session_id: str, user_input: str) -> str
        Generate a response to the user's input within a given session.
    getHistory(session_id: str) -> list[tuple[str, str]]
        Retrieve the chat history for a given session as a list of (user_input, bot_response) tuples.
    """
    @abstractmethod
    def answer(self, session_id : str, user_input : str):
        pass
    
    @abstractmethod
    def getHistory(self, session_id : str) -> list[tuple[str, str]]:
        pass

    def clearHistory(self, session_id : str) -> None:
        pass