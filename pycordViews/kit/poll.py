from ..views.easy_modified_view import EasyModifiedViews
from discord.ui.button import Button, ButtonStyle
from discord import Emoji, PartialEmoji, Member
from discord.abc import GuildChannel
from typing import Optional, Callable, Union


class Poll:

    def __init__(self, timeout: Optional[float], unique_vote: bool = True):
        """
        Class instance to make poll with buttons
        :param timeout: Time before end the view
        :param unique_vote: Set True to make vote unchangeable
        """
        self.yes_count: int = 0
        self.no_count: int = 0
        self.__unique_vote: bool = unique_vote
        self.__view = EasyModifiedViews(disabled_on_timeout=True, timeout=timeout)
        self.__button_yes = Button(label='Yes', emoji='✅', custom_id='Poll_yes', style=ButtonStyle.green)
        self.__button_no = Button(label='No', emoji='❌', custom_id='Poll_no', style=ButtonStyle.red)
        self.__view.add_items(self.__button_yes, self.__button_no)
        self.__view.set_callable('Poll_yes', _callable=self.yes)
        self.__view.set_callable('Poll_no', _callable=self.no)
        self.__clicked_members: list[int] = []

    def set_yes_button(self, label: Optional[str],
                       emoji: Optional[str, Emoji, PartialEmoji],
                       style: Optional[ButtonStyle],
                       callable: Optional[Callable]):
        """
        Set yes button parameters (he didn't change dynamically if the view was sent before)
        :param label: Button label
        :param emoji: Button emoji
        :param style: Button style
        :param callable: Asynchronous function linked to the button interaction. It's called when the button is pressed
        """
        self.__button_yes.emoji = emoji if emoji is not None else self.__button_yes.emoji
        self.__button_yes.style = style if style is not None else self.__button_yes.style
        self.__button_yes.label = label if label is not None else self.__button_yes.label
        if callable is not None:
            self.__view.set_callable(self.__button_yes.custom_id, _callable=callable)

    def set_no_button(self, label: Optional[str],
                       emoji: Optional[str, Emoji, PartialEmoji],
                       style: Optional[ButtonStyle],
                       callable: Optional[Callable]):
        """
        Set no button parameters (he didn't change dynamically if the view was sent before)
        :param label: Button label
        :param emoji: Button emoji
        :param style: Button style
        :param callable: Asynchronous function linked to the button interaction. It's called when the button is pressed
        """
        self.__button_no.emoji = emoji if emoji is not None else self.__button_no.emoji
        self.__button_no.style = style if style is not None else self.__button_no.style
        self.__button_no.label = label if label is not None else self.__button_no.label
        if callable is not None:
            self.__view.set_callable(self.__button_no.custom_id, _callable=callable)

    async def yes(self, button, interaction):
        """
        Base asynchronous function when "yes" button is pressed.
        Increment “yes_count” attribute when pressed and respond with an ephemeral message.
        This function can be changed.
        """
        if self.__unique_vote and interaction.user.id in self.__clicked_members:
            await interaction.response.send_message(f"You have already voted !", ephemeral=True)
            return
        self.yes_count += 1
        self.__clicked_members.append(interaction.user.id)
        await interaction.response.send_message(f"You have selected : {button.name}", ephemeral=True)

    async def no(self, button, interaction):
        """
        Base asynchronous function when "no" button is pressed.
        Increment “yes_count” attribute when pressed and respond with an ephemeral message.
        This function can be changed.
        """
        if self.__unique_vote and interaction.user.id in self.__clicked_members:
            await interaction.response.send_message(f"You have already voted !", ephemeral=True)
            return
        self.yes_count += 1
        self.__clicked_members.append(interaction.user.id)
        await interaction.response.send_message(f"You have selected : {button.name}", ephemeral=True)

    async def send(self, target: Union[Member, GuildChannel], *args, **kwargs):
        """
        Send the view to the target. Pass common send argument like "content" or "embed" in addition.
        :param target: The current target.
        """
        await self.__view.send(target=target, *args, **kwargs)

    @property
    def get_view(self) -> EasyModifiedViews:
        """
        Get the current view
        """
        return self.__view
