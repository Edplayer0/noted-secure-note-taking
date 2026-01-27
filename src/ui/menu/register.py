"""Register module, which adds the functions to the menu"""

from typing import Callable


class Register:
    """Register class"""

    _menu = None

    @classmethod
    def config_menu(cls, menu) -> None:
        """Configure the menu instance"""

        cls._menu = menu

    @classmethod
    def registry(cls, name: str) -> Callable:
        """Adds a function to the menu throught the decorator"""

        def decorator(func: Callable) -> None:

            cls._menu.add_button(name, func)

        return decorator

    @staticmethod
    def load_functions() -> None:
        """Import the functs module so the
        functions are defined and registered"""

        # pylint: disable=import-outside-toplevel
        # pylint: disable=unused-import
        import src.ui.menu.functs
