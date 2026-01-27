"""App communications mediator"""

from typing import List, Dict, Callable, TypeVar
from src.mediator.mediator import Mediator

T = TypeVar("T")


class AppMediator(Mediator):
    """App communications mediator"""

    def __init__(self):

        self.handlers: Dict[str, List[Callable]] = {}

    def add_handler(self, event: str, handler: Callable, priority: int = 3) -> None:
        if not event in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(
            (
                priority,
                handler,
            )
        )

    def call_event(self, event: str, data: T | None = None) -> List[T] | T:

        response = []

        if event in self.handlers:
            for _, handler in sorted(self.handlers[event], key=lambda i: i[0]):

                if data is None:
                    result = handler()

                else:
                    try:
                        result = handler(data)
                    except TypeError:
                        result = handler()

                if result:
                    response.append(result)

        if len(response) == 1:
            response = response[0]

        return response
