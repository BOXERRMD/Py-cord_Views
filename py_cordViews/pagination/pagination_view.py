from ..views.easy_modified_view import EasyModifiedViews
from discord import ButtonStyle, Interaction
from discord.ui import Button
from .errors import PageNumberNotFound

from typing import Union, Any


class Pagination:
    """
    Class
    -------------
    Allows you to easily setup a view pagination
    """

    def __init__(self, timeout: Union[float, None] = None, disabled_on_timeout:bool = False):
        """
        Initialisation for pagination
        :param timeout: The time before disable items on the view
        :param disabled_on_timeout: If timeout is done, disable all items
        """
        self.__view = EasyModifiedViews(timeout, disabled_on_timeout=disabled_on_timeout)

        self.__view.add_items(Button(label='⏮', row=0, custom_id='back+', style=ButtonStyle.blurple))
        self.__view.add_items(Button(label='◀', row=0, custom_id='back', style=ButtonStyle.blurple))
        self.__view.add_items(Button(label='▶', row=0, custom_id='forward', style=ButtonStyle.blurple))
        self.__view.add_items(Button(label='⏭', row=0, custom_id='forward+', style=ButtonStyle.blurple))
        self.__view.set_callable('back+', 'back', 'forward', 'forward+', coroutine=self.__turn_page)

        self.__pages: dict[str, tuple[tuple[Any, ...], dict]] = {}
        self.__current_page: int = 1


    def add_page(self, *args, **kwargs) -> None:
        """
        Adds a page as if this function directly sent the message
        """
        self.__pages[str(len(self.__pages)+1)] = (args, kwargs)

    def delete_pages(self, *page_numbers: Union[str, int]): ######################## A FINIR, il supprime la bonne page mais cela décale les autres car les pages sont parqué par les clé du dict
        """
        Deletes pages in the order in which they were added
        """
        for page_number in page_numbers:
            number = str(page_number)
            if number not in self.__pages.keys():
                raise PageNumberNotFound(number)

            del self.__pages[number]

        for page in self.__pages.keys(): # if faut arriver à combler les trous laissé par la suppression si possible
            self.__pages[page]



    async def __turn_page(self, interaction: Interaction):
        """
        Turn the page when button is pressed
        """
        page_count = len(self.__pages)

        if page_count <= 1:
            await self.__view.shutdown()
            await interaction.response.defer(invisible=True)
            return

            # Update the current page based on the button pressed

        if interaction.custom_id == 'back+':  # Go to the first page
            self.__current_page = 1

        elif interaction.custom_id == 'back':  # Go to the previous page
            self.__current_page = max(1, self.__current_page - 1)

        elif interaction.custom_id == 'forward':  # Go to the next page
            self.__current_page = min(page_count, self.__current_page + 1)

        elif interaction.custom_id == 'forward+':  # Go to the last page
            self.__current_page = page_count


        await interaction.message.edit(

            *self.__pages[self.__current_page][0],

            **self.__pages[self.__current_page][1]

        )

        # Acknowledge the interaction
        await interaction.response.defer(invisible=True)

    @property
    def get_view(self) -> EasyModifiedViews:
        """
        Get the view of pagination
        """
        return self.__view

    @property
    def get_page(self) -> int:
        """
        Get the number of showed page
        """
        return self.__current_page
