"""Mediator abstraction"""

from abc import ABC, abstractmethod
from typing import Any, Callable


class Mediator(ABC):
    """Mediator abstaction"""

    @abstractmethod
    def add_handler(self, event: str, handler: Callable, priority: int) -> None:
        """Appends a event"""

    @abstractmethod
    def call_event(self, event: str, data: Any = None) -> Any:
        """Calls a event and returns it response"""
