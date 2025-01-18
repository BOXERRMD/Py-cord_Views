from discord import Interaction, ApplicationContext, Message
from discord.ui import View, Item
from typing import Union, Callable, Coroutine

from py_cordViews.typeViews import T_views
from .errors import CustomIDNotFound



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
        self.__callback: dict[str, dict[str, Union[Callable[[Interaction], None], T_views]]] = {}
        self.__ctx: Union[Message, Interaction] = None

    def __check_custom_id(self, custom_id: str) -> None:
        """
        Check if the custom_id is alive
        :param custom_id: ID to find
        :raise: CustomIDNotFound
        """
        if custom_id not in self.__callback.keys():
            raise CustomIDNotFound()

    async def respond(self, ctx: ApplicationContext, *args, **kwargs):
        """
        Respond at the ApplicationContext
        """
        self.__ctx = await ctx.respond(*args, **kwargs)

    def add_items(self,
                   *items: T_views) -> None:
        """
        Add all items in the View.
        custom_id REQUIRED !
        """

        for ui in items:

            self.__callback[ui.custom_id] = {'ui': ui, 'func': None}
            self.add_item(ui)

    async def update_items(self, *items: T_views):
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

        await self.__update()

    def set_callable_decorator(self, custom_id: str):
        """
        Decorator to set up a coroutine for the item

        **Interaction parameter is required in coroutine function !**

        view = EasyModifiedViews(None)
        view.add_view(discord.ui.Button(label='coucou', custom_id='test_ID'))

        @view.set_callable_decorator(custom_id='test_ID')

        async def rep(**interaction**):
            await interaction.response.send_message('coucou !!!')

        await ctx.respond('coucou', view=view)

        :param custom_id: item ID of the view
        """

        def decorator(coroutine: Coroutine):
            self.__check_custom_id(custom_id)

            self.__callback[custom_id]['func'] = coroutine
            return coroutine

        return decorator

    def set_callable(self, custom_id: str, coroutine: Coroutine):
        """
        set up a coroutine for items
        :param custom_id: items ID of the view
        :param coroutine: The coroutine linked

        **Interaction parameter is required in coroutine function !**

        view = EasyModifiedViews(None)
        view.add_view(discord.ui.Button(label='coucou', custom_id='test_ID'))

        async def rep(**interaction**):
            await interaction.response.send_message('coucou !!!')

        view.set_callable(custom_id='test_ID', coroutine=rep)
        await ctx.respond('coucou', view=view)
        """
        self.__check_custom_id(custom_id)

        self.__callback[custom_id]['func'] = coroutine

    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Func to apply items
        """
        print(self.__callback[interaction.custom_id])
        await self.__callback[interaction.custom_id]['func'](interaction)

        return True

    async def shutdown(self) -> None:
        """
        Disable all items (ui) in the view
        """
        self.disable_all_items()
        await self.__update()

    async def disable_item(self, *custom_ids: str):
        """
        Disable partial items in the view
        :param custom_ids: custom ids of all items to deactivate
        """

        self.disable_all_items(exclusions=[self.get_item(id_) for id_ in self.__callback.keys() if id_ not in custom_ids])

    async def delete_items(self, clear_all: bool = False, *custom_ids: str):
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

        await self.__update()

    def on_timeout(self) -> None:
        """
        Called if timeout view is finished
        """
        if self.__disabled_on_timeout:
            self.shutdown()

    async def __update(self):
        """
        Update the View on the attached message.
        """
        if self.message:
            await self.message.edit(view=self)

        else:
            await self.__ctx.edit(view=self)

    @property
    def get_uis(self) -> list[T_views]:
        """
        Get all uis in the view
        """
        return [i['ui'] for i in self.__callback.values()]

    def get_ui(self, custom_id: str) -> T_views:
        """
        Get an ui in the view
        :raise: CustomIDNotFound
        """
        self.__check_custom_id(custom_id)
        return self.__callback[custom_id]['ui']
