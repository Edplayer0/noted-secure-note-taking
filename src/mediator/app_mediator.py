"""App communications mediator"""

from typing import List, Dict, Callable, TypeVar
from mediator.mediator import Mediator

T = TypeVar("T")


class AppMediator(Mediator):
    """App communications mediator"""

    def __init__(self):

        self.handlers: Dict[str, List[Callable]] = {}

    def add_handler(self, event: str, handler: Callable) -> None:
        if not event in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)

    def call_event(self, event: str, data: T | None = None) -> List[T] | T:

        response = []

        if event in self.handlers:
            for handler in self.handlers[event]:

                # sig = signature(handler)
                # num_args = len(sig.parameters)

                # try:
                #     if num_args == 0:  # No toma args
                #         result = handler()
                #     elif data is not None:  # Toma args y hay data
                #         result = handler(data)
                #     else:  # Toma args pero no hay data
                #         result = handler()
                # except TypeError:
                #     # Fallback: intenta sin args si falla con data
                #     result = handler()

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
