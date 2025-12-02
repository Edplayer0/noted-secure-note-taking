"""Database communications mediator"""

from typing import Any, List, Dict, Callable
from mediator.mediator import Mediator


class DatabaseMediator(Mediator):
    """Database mediator"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.services: List[Any] = []
            self.handlers: Dict[str, Callable] = {}

            self._initialized = True

    def add_service(self, service: Any) -> None:
        self.services.append(service)
        service.mediator = self

    def add_event(self, event: str, handler: Callable) -> None:
        if not event in self.handlers:
            self.handlers[event] = handler

    def call_event(self, event: str, data: Any = None) -> Any:
        if event in self.handlers:
            if data:
                return self.handlers[event](data)
            return self.handlers[event]()
        return None
