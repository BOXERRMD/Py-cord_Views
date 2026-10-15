from discord import File, Embed
from immutableType import callable_, NoneType
from ..views import EasyModifiedViews
from typing import Optional, Callable, Union, Any, Coroutine
from types import FunctionType
from inspect import iscoroutinefunction
from asyncio import create_task, Task

annot_type_content = Optional[Union[str, Callable[[..., Any], str], Callable[[..., Any], Coroutine[Any, Any, str]]]]
annot_type_embed = Optional[Union[Embed, Callable[[..., Any], Embed], Callable[[..., Any], Coroutine[Any, Any, Embed]]]]
annot_type_embeds = Optional[Union[list[Embed], Callable[[..., Any], list[Embed]], Callable[[..., Any], Coroutine[Any, Any, list[Embed]]]]]
annot_type_file = Optional[Union[File, Callable[[..., Any], File], Callable[[..., Any], Coroutine[Any, Any, File]]]]
annot_type_files = Optional[Union[list[File], Callable[[..., Any], list[File]], Callable[[..., Any], Coroutine[Any, Any, list[File]]]]]

class Page:

    @callable_(is_class=True, kwargs_types={
        'view': [NoneType, EasyModifiedViews],
        'content': [NoneType, str, FunctionType],
        'embed': [NoneType, Embed, FunctionType],
        'embeds': [NoneType, list, FunctionType],
        'file': [NoneType, File, FunctionType],
        'files': [NoneType, list, FunctionType],
        'args_content': [NoneType, tuple],
        'args_embeds': [NoneType, tuple],
        'args_files': [NoneType, tuple]
    })

    def __init__(self, view: Optional[EasyModifiedViews] = None,
                 content: annot_type_content = None,
                 embed: annot_type_embed = None,
                 embeds: annot_type_embeds = None,
                 file: annot_type_file = None,
                 files: annot_type_files = None,
                 args_content: Optional[tuple] = None,
                 args_embeds: Optional[tuple] = None,
                 args_files: Optional[tuple] = None):
        """
        Init Page instance from Pagination class
        """
        self.__view: EasyModifiedViews = view if view is not None else EasyModifiedViews()
        self.content: annot_type_content = content
        self.embeds: tuple[annot_type_embed,
                    annot_type_embeds] \
                        = (embed, embeds)
        self.files: tuple[annot_type_file,
                    annot_type_files] \
                        = (file, files)
        self.args_content: tuple = args_content or ()
        self.args_embeds: tuple = args_embeds or ()
        self.args_files: tuple = args_files or ()

    async def __make_embeds(self,
                      embed: annot_type_embed,
                      embeds: annot_type_embeds) -> list[Embed]:
        """
        Make the embed(s) for the page
        """
        final_embeds: list[Embed] = []
        if embed is not None:
            if iscoroutinefunction(embed):
                task: Task = create_task(embed(*self.args_embeds))
                await task
                final_embeds.append(task.result())
            else:
                final_embeds.append(embed(*self.args_embeds) if callable(embed) else embed)
        if embeds is not None:
            if iscoroutinefunction(embeds):
                task: Task = create_task(embeds(*self.args_embeds))
                await task
                final_embeds.extend(task.result())
            else:
                final_embeds.extend(embeds(*self.args_embeds) if callable(embeds) else embeds)
        return final_embeds

    async def __make_files(self,
                     file: annot_type_file,
                     files: annot_type_files) -> list[File]:
        """
        Make the file(s) for the page
        """
        final_files: list[File] = []
        if file is not None:
            if iscoroutinefunction(file):
                task: Task = create_task(file(*self.args_files))
                await task
                final_files.append(task.result())
            else:
                final_files.append(file(*self.args_files) if callable(file) else file)
        if files is not None:
            if iscoroutinefunction(files):
                task: Task = create_task(files(*self.args_files))
                await task
                final_files.extend(task.result())
            else:
                final_files.extend(files(*self.args_files) if callable(files) else files)
        return final_files

    async def __make_content(self, content: annot_type_content) -> Optional[str]:
        """
        Make the content for the page
        """
        if content is not None:
            if iscoroutinefunction(content):
                task: Task = create_task(content(*self.args_content))
                await task
                return task.result()
            else:
                return content(*self.args_content) if callable(content) else content
        return None

    async def build_page(self) -> dict:
        """
        Build the page to send it
        """
        return {
            "content": await self.__make_content(self.content),
            "embeds": await self.__make_embeds(*self.embeds),
            "files": await self.__make_files(*self.files),
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
