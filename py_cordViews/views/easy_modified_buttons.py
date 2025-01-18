from discord import Interaction
from discord.ui import View, Item
from typing import Union, Callable, Coroutine

from py_cordViews.typeViews import T_views
from .errors import CustomIdRequired, CustomIDNotFound



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
        self.__callback: dict[str, Callable[[Interaction], None]] = {}

    def add_views(self,
                   *views: T_views) -> None:
        """
        Add all items in the View.
        custom_id REQUIRED !
        """

        for ui in views:

            self.__callback[ui.custom_id] = None
            self.add_item(ui)

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
            if custom_id not in self.__callback.keys():
                raise CustomIDNotFound

            self.__callback[custom_id] = coroutine
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
        if custom_id not in self.__callback.keys():
            raise CustomIDNotFound

        self.__callback[custom_id] = coroutine


    async def interaction_check(self, interaction: Interaction) -> bool:
        """
        Func to apply items
        """
        await self.__callback[interaction.custom_id](interaction)

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

    def on_timeout(self) -> None:
        """
        Called if timeout view is finished
        """
        if self.__disabled_on_timeout:
            self.shutdown()


    async def __update(self):

        print(self.message)
        await self.message.edit(view=self)



