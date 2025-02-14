from discord.components import ComponentType
from discord.ui import Select
from discord import MISSING, Emoji, PartialEmoji
from typing import Callable, Union

from .errors import NotCoroutineError, ComponentTypeError


class Menu:

    def __init__(self, menu_type: ComponentType, selectmenu: "SelectMenu", **kwargs):
        """
        A basic menu from selectMenu class
        """
        self.__menu: Select = Select(select_type=menu_type, **kwargs)
        self.__selectMenu = selectmenu

    def set_callable(self, _callable: Callable) -> "Menu":
        """
        Add a coroutine to the menu
        """
        if not isinstance(_callable, Callable):
            raise NotCoroutineError(_callable)

        self.__selectMenu.set_callable(self.__menu.custom_id, _callable=_callable)
        return self

    def add_option(self, label: str, value: str = MISSING, description: Union[str, None] = None, emoji: Union[str, Emoji, PartialEmoji, None] = None, default: bool = False) -> "Menu":
        """
        Add an option to choice.
        Only from string_select type !
        """
        if self.__menu.type != ComponentType.string_select:
            raise ComponentTypeError()

        self.__menu.add_option(label=label, value=value, description=description, emoji=emoji, default=default)
        return self

    @property
    def component(self) -> Select:
        """
        Get the component
        """
        return self.__menu

    @property
    def callable(self) -> Callable:
        """
        Get the callable link to the menu
        """
        return self.__callable

    @callable.setter
    def callable(self, _callable: Callable):
        """
        Set the callable link to menu
        """