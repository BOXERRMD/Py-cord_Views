from discord import File, Embed
from immutableType import callable_, NoneType
from ..views import EasyModifiedViews
from typing import Optional, Callable, Union
from types import FunctionType

class Page:

    @callable_(is_class=True, kwargs_types={
        'view': [NoneType, EasyModifiedViews],
        'content': [NoneType, str, FunctionType],
        'embed': [NoneType, Embed, FunctionType],
        'embeds': [NoneType, list, FunctionType],
        'file': [NoneType, File, FunctionType],
        'files': [NoneType, list, FunctionType]})

    def __init__(self, view: Optional[EasyModifiedViews] = None,
                 content: Optional[Union[str, Callable[[], str]]] = None,
                 embed: Optional[Union[Embed, Callable[[], Embed]]] = None,
                 embeds: Optional[Union[list[Embed], Callable[[], list[Embed]]]] = None,
                 file: Optional[Union[File, Callable[[], File]]] = None,
                 files: Optional[Union[list[File], Callable[[], list[File]]]] = None):
        """
        Init Page instance from Pagination class
        """
        self.__view: EasyModifiedViews = view if view is not None else EasyModifiedViews()
        self.content: Optional[Union[str, Callable[[], str]]] = content
        self.embeds: tuple[Optional[Union[Embed, Callable[[], Embed]]],
                    Optional[Union[list[Embed], Callable[[], list[Embed]]]]] \
                        = (embed, embeds)
        self.files: tuple[Optional[Union[File, Callable[[], File]]],
                    Optional[Union[list[File], Callable[[], list[File]]]]] \
                        = (file, files)

    @staticmethod
    def __make_embeds(embed: Optional[Union[Embed, Callable[[], Embed]]],
                     embeds: Optional[Union[list[Embed], Callable[[], list[Embed]]]]) -> list[Embed]:
        """
        Make the embed(s) for the page
        """
        final_embeds: list[Embed] = []
        if embed is not None:
            final_embeds.append(embed() if callable(embed) else embed)
        if embeds is not None:
            final_embeds.extend(embeds() if callable(embeds) else embeds)
        return final_embeds

    @staticmethod
    def __make_files(file: Optional[Union[File, Callable[[], File]]],
                    files: Optional[Union[list[File], Callable[[], list[File]]]]) -> list[File]:
        """
        Make the file(s) for the page
        """
        final_files: list[File] = []
        if file is not None:
            final_files.append(file() if callable(file) else file)
        if files is not None:
            final_files.extend(files() if callable(files) else files)
        return final_files

    def build_page(self) -> dict:
        """
        Build the page to send it
        """
        return {
            "content": self.content() if callable(self.content) else self.content,
            "embeds": self.__make_embeds(*self.embeds),
            "files": self.__make_files(*self.files),
            "view": self.__view
        }

    @property
    def get_page_view(self) -> EasyModifiedViews:
        """
        Get the current page view
        """
        return self.__view

    @get_page_view.setter
    def get_page_view(self, new_view: EasyModifiedViews):
        """
        Set a new view for the page
        """
        if not isinstance(new_view, EasyModifiedViews):
            raise TypeError(f"New page vien must be EasyModifiedViews class instance, not {type(new_view)}")

        self.__view = new_view
