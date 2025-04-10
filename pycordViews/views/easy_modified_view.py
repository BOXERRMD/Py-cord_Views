from __future__ import annotations
from discord import Interaction, ApplicationContext, Message, Member, TextChannel
from discord.ui import View, Item
from typing import Union, Callable, TYPE_CHECKING

from .errors import CustomIDNotFound

if TYPE_CHECKING:
    from ..menu.selectMenu import SelectMenu
    from ..pagination.pagination_view import Pagination


class EasyModifiedViews(View):
    """
    Class
    -------------
    Allows you to easily modify and replace an ui.
    """

    def __init__(self, timeout: Union[float, None] = None, disabled_on_timeout: bool = False, *items: Item):
        """
        Init a Class view for Discord UI
        :param timeout: The time before ui disable
        """
        super().__init__(*items, timeout=timeout)
        self.__timeout: Union[float, None] = timeout
        self.__disabled_on_timeout: bool = disabled_on_timeout
        self.__callback: dict[str, dict[str, Union[Callable[[Interaction], None], Item]]] = {}
        self.__ctx: Union[Message, Interaction] = None

    def __check_custom_id(self, custom_id: str) -> None:
        """
        Check if the custom_id is alive
        :param custom_id: ID to find
        :raise: CustomIDNotFound
        """
        if custom_id not in self.__callback.keys():
            raise CustomIDNotFound()

    async def respond(self, ctx: ApplicationContext, *args, **kwargs) -> None:
        """
        Respond at the ApplicationContext
        """
        self.__ctx = await ctx.respond(*args, **kwargs)

    async def send(self, target: Union[Member, TextChannel], *args, **kwargs) -> None:
        """
        Send at the target
        """
        self.__ctx = await target.send(*args, **kwargs)

    def add_items(self,
                   *items: Union[Item, SelectMenu, Pagination]) -> "EasyModifiedViews":
        """
        Add all items in the View.
        """

        for ui in items:

            if type(ui).__name__ in ('SelectMenu', 'Pagination'):
                for item in ui.get_view.items:
                    self.add_items(item)
                    self.set_callable(item.custom_id, _callable=ui.get_callable(item.custom_id))

            else:
                self.__callback[ui.custom_id] = {'ui': ui, 'func': None}
                self.add_item(ui)

        return self

    async def update_items(self, *items: Item) -> "EasyModifiedViews":
        """
        Update all views.
        Append items if custom_ids not in the view
        Update items if custom_ids in the view
        :param items: items to update
        """

        for item in items:
            try:
                self.__check_custom_id(item.custom_id)
                self.__callback[item.custom_id]['ui'] = item

            except CustomIDNotFound:
                self.add_items(item)

        await self._update()
        return self

    def set_callable_decorator(self, custom_id: str):
        """
        Decorator to set up a callable for the item

        **Interaction parameter is required in coroutine function !**

        view = EasyModifiedViews(None)
        view.add_view(discord.ui.Button(label='coucou', custom_id='test_ID'))

        @view.set_callable_decorator(custom_id='test_ID')

        async def rep(**UI**, **interaction**):
            await interaction.response.send_message('coucou !!!')

        await ctx.respond('coucou', view=view)

        :param custom_id: item ID of the view
        """

        def decorator(_callable: Callable):
            self.__check_custom_id(custom_id)

            self.__callback[custom_id]['func'] = _callable
            return _callable

        return decorator

    def set_callable(self, *custom_ids: str, _callable: Callable):
        """
        set up a callable for items
        :param custom_ids: items IDs of the view
        :param _callable: The callable linked

        **UI and Interaction parameter is required in callable function !**

        view = EasyModifiedViews(None)

        view.add_view(discord.ui.Button(label='coucou', custom_id='test_ID'))

        async def rep(**UI**, **interaction**):
            await interaction.response.send_message('coucou !!!')

        view.set_callable(custom_id='test_ID', callable=rep)
        await ctx.respond('coucou', view=view)
        """
        for custom_id in custom_ids:
            self.__check_custom_id(custom_id)

            self.__callback[custom_id]['func'] = _callable

    def get_callable(self, custom_id: str) -> Union[Callable, None]:
        """
        Get the callable UI
        :param custom_id: UI ID
        """
        self.__check_custom_id(custom_id)
        return self.__callback[custom_id]['func']

    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Func to apply items
        """
        func = self.__callback[interaction.custom_id]['func']

        if func is not None:
            return await func(self.__callback[interaction.custom_id]['ui'], interaction)

        else:
            await interaction.response.defer(invisible=True)

        return True

    async def shutdown(self) -> None:
        """
        Disable all items (ui) in the view
        """
        self.disable_all_items()
        await self._update()

    async def disable_items(self, *custom_ids: str) -> None:
        """
        Disable partial items in the view
        :param custom_ids: custom ids of all items to deactivate
        """

        self.disable_all_items(exclusions=[self.get_item(id_) for id_ in self.__callback.keys() if id_ not in custom_ids])
        await self._update()

    async def enable_items(self, *custom_ids: str) -> None:
        """
        Enabl partial items in the view
        :param custom_ids: custom ids of all items to activate
        """
        self.enable_all_items(
            exclusions=[self.get_item(id_) for id_ in self.__callback.keys() if id_ not in custom_ids])
        await self._update()

    async def full_enable_items(self) -> None:
        """
        Enable all items in the view
        """
        self.enable_all_items()
        await self._update()


    async def switch_status_items(self):
        """
        Switch status for all items
        Enable -> Disable
        Disable -> Enable
        """

        for key, in self.__callback.keys():
            self.__callback[key]['ui'].disabled = not self.__callback[key]['ui'].disabled

        await self._update()


    def is_items_disabled(self, *custom_ids: str) -> bool:
        """
        Return True if all items are disabled
        """

        for custom_id in custom_ids:
            self.__check_custom_id(custom_id)
            if not self.__callback[custom_id]['ui'].disabled:
                return False

        return True


    def is_items_enabled(self, *custom_ids: str) -> bool:
        """
        Return True il aff items are enabled
        """

        for custom_id in custom_ids:
            self.__check_custom_id(custom_id)
            if self.__callback[custom_id]['ui'].disabled:
                return False

        return True


    async def delete_items(self, clear_all: bool = False, *custom_ids: str) -> None:
        """
        Delete an item on the view
        :param custom_ids: IDs of items to delete
        :param clear_all: Clear all items in the view
        :raise: CustomIDNotFound
        """
        if clear_all:
            self.clear_items()

        else:

            for custom_id in custom_ids:
                self.__check_custom_id(custom_id)
                self.remove_item(self.get_item(custom_id))

        await self._update()

    def on_timeout(self) -> None:
        """
        Called if timeout view is finished
        """
        if self.__disabled_on_timeout:
            self.shutdown()

    async def _update(self) -> None:
        """
        Update the View on the attached message.
        """
        if self.is_finished():
            return

        if self.message:
            await self.message.edit(view=self)

        elif self.__ctx:
            await self.__ctx.edit(view=self)

        else:
            return

    @property
    def get_uis(self) -> list[Item]:
        """
        Get all uis in the view
        """
        return [i['ui'] for i in self.__callback.values()]

    def get_ui(self, custom_id: str) -> Item:
        """
        Get an ui in the view
        :raise: CustomIDNotFound
        """
        self.__check_custom_id(custom_id)
        return self.__callback[custom_id]['ui']

    def __str__(self):
        return str(self.__callback)

    @property
    def items(self) -> tuple[Item]:
        return tuple([i['ui'] for i in self.__callback.values()])
