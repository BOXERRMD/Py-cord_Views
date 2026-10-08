from discord.ui import BaseView, ViewItem
from discord import Interaction, Message, Role
from typing import Optional, Union, Callable, Any

from .errors import CustomIDNotFound

class EasyModifiedBaseView(BaseView):
    """
    Class
    -------------
    Allows you to easily modify and replace a baseui.
    """

    def __init__(self, timeout: Optional[float] = None, disabled_on_timeout: bool = False, call_on_timeout: Optional[Callable] = None, store: bool = True, *items: ViewItem):
        """
        Init a Class view for Discord UI
        :param timeout: The time before ui disable
        :param disabled_on_timeout:  view if timeout is reached
        :param call_on_timeout: asynchronous function to call after view timed-out
        """
        super().__init__(*items, timeout=timeout, store=store)
        self.__timeout: Optional[float] = timeout
        self.__disabled_on_timeout: bool = disabled_on_timeout
        self.__callback: dict[str, dict[str, Union[Callable[[Interaction], None], ViewItem, Any]]] = {}
        self.__ctx: Optional[Union[Message, Interaction]] = None
        self.__call_on_timeout: Callable = call_on_timeout

    def __check_custom_id(self, custom_id: str) -> None:
        """
        Check if the custom_id is alive
        :param custom_id: ID to find
        :raise: CustomIDNotFound
        """
        if custom_id not in self.__callback.keys():
            raise CustomIDNotFound()

    def add_items(self, *items: ViewItem) -> None:
        """
        Add items to the view
        :param items: items to add
        """
        for ui in items:

            if ui is None:
                continue

            if isinstance(ui, ViewItem):
                self.__callback[ui.custom_id] = {
                     'ui': ui,
                     'func': None,
                     'data': {},
                     'autorised_roles': None,
                     'autorised_key': None
                }
                self.add_item(ui)

    async def on_timeout(self) -> None:
        try:
            if self.__disabled_on_timeout:
                self.disable_all_items()
            if self.__call_on_timeout is not None:
                await self.__call_on_timeout(self.__ctx)
        finally:
            self.__cleanup()

    def __cleanup(self) -> None:
        self.clear_items()
        self.__callback.clear()
        self.__call_on_timeout = None
        self.__ctx = None
        self.message = None
        self.parent = None
        self.stop()

    def set_callable(self, *custom_ids: str,
                     _callable: Callable,
                     data: Optional[dict[str, Any]] = None,
                     autorised_roles: Optional[list[Union[int, Role]]] = None,
                     autorised_key: Optional[Callable] = None):
        """
        set up a callable for items
        :param custom_ids: items IDs of the view
        :param _callable: The asynchronous callable linked. Take UI (Button, Select...) and Interaction parameters.
        :param data: Add any data to pass in called function.
        :param autorised_roles: Any role ID allowed to interact with the view
        :param autorised_key: Callable function to check anything. The function get the current interaction and data passed in parameter

        **UI, Interaction and data parameter is required in callable function !**

        view = EasyModifiedBaseViews(None)

        view.add_view(discord.ui.Button(label='coucou', custom_id='test_ID'))

        async def rep(**UI**, **interaction**, data: dict[str, Any]):
            await interaction.response.send_message(data['message'])

        view.set_callable(custom_id='test_ID', callable=rep, data={'message': 'Hello !'})
        await ctx.respond('coucou', view=view)
        """
        for custom_id in custom_ids:
            self.__check_custom_id(custom_id)

            self.__callback[custom_id]['func'] = _callable
            self.__callback[custom_id]['data'] = data if data is not None else {}
            self.__callback[custom_id]['autorised_key'] = autorised_key
            if autorised_roles is not None:
                self.__callback[custom_id]['autorised_roles'] = [role.id if isinstance(role, Role) else role for role in
                                                                 autorised_roles if isinstance(role, (Role, int))]
            else:
                self.__callback[custom_id]['autorised_roles'] = None
