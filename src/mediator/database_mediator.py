"""Database communications mediator"""

from typing import Any, List, Dict, Callable, TypeVar
from mediator.mediator import Mediator

T = TypeVar("T")
HandlerResult = List[T] | T


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
            self.handlers: Dict[str, List[Callable]] = {}

            self._initialized = True

    def add_service(self, service: Any) -> None:
        self.services.append(service)
        service.mediator = self

    def add_handler(self, event: str, handler: Callable) -> None:
        if not event in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def call_event(self, event: str, data: T | None = None) -> HandlerResult:

        response = []

        if event in self.handlers:
            for handler in self.handlers[event]:
                if data:
                    result = handler(data)
                    if result:
                        response.append(result)
                else:
                    result = handler()
                    if result:
                        response.append(result)

        if len(response) == 1:
            response = response[0]

        return response
