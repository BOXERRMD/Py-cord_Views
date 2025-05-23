# Py-cord_Views
 Views for py-cord library

# Paginator
The paginator instance is used to create a view acting as a “book”, with pages that can be turned using buttons.
## `Paginator`
> ```python
> Paginator(timeout: Union[float, None] = None, disabled_on_timeout: bool = False)`
> ```
> > **Method** `add_page(*args, **kwargs) -> Pagination` : add a new page with send message function parameters _(content, embed, embeds, files...)_
>
> > **Method** `delete_pages(*page_numbers: Union[str, int]) -> Pagination` : Deletes pages in the order in which they were added _(start to 0)_
> 
> > **Method** `send(target: Union[Member, TextChannel]) -> Any` : Send the pagination in dm member or channels
> 
> > **Method** `respond(ctx: Union[ApplicationContext, Interaction]) -> Any` : Respond at slash command call
> 
> > **@property** `get_view -> EasyModifiedViews` : Return the pagination view. Can be used in `view` parameter to setup a view
> 
> > **@property** `get_page -> int` : get the showed page number

```python
from pycordViews.pagination import Pagination
import discord

intents = discord.Intents.all()
bot = discord.AutoShardedBot(intents=intents)

@bot.command(name="My command paginator", description="...")
async def pagination_command(ctx):
    """
    Create a command pagination
    """
    pages: Pagination = Pagination(timeout=None, disabled_on_timeout=False)
    
    pages.add_page(content="It's my first page !!", embed=None)# reset embed else he show the embed of the page after
    
    embed = discord.Embed(title="My embed title", description="..........")
    pages.add_page(content=None, embed=embed) # reset content else he show the content of the page before

    pages.add_page(content="My last page !", embed=None)# reset embed else he show the embed of the page before

    await pages.respond(ctx=ctx) # respond to the command
    await pages.send(target=ctx.author) # send the message to the command author

bot.run("Your token")
```

# SelectMenu
The SelectMenu instance is used to create drop-down menus that can be easily modified at will.

## `SelectMenu`
> ```python
> SelectMenu(timeout: Union[float, None] = None, disabled_on_timeout: bool = False)`
> ```
> > **Method** `add_string_select_menu(custom_id: str = None, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled=False, row=None) -> Menu` : Add a string select menu in the ui. Return Menu instance to set options 
> 
> > **Method** `add_user_select_menu(custom_id: str = None, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled=False, row=None) -> Menu` : Add a user select menu in the ui. Return Menu instance to set options 
> 
> > **Method** `add_role_select_menu(custom_id: str = None, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled=False, row=None) -> Menu` Add a role select menu in the ui. Return Menu instance to set options
> 
> > **Method** `add_mentionnable_select_menu(custom_id: str = None, placeholder: str = None, min_values: int = 1, max_values: int = 1, disabled=False, row=None) -> Menu` : Add a mentionable select menu in the ui. Return Menu instance to set options
> 
> > **Method** `set_callable(*custom_ids: str, _callable: Union[Callable, None], data: Optional[dict[str, Any]], autorised_roles : Optional[list[Union[int, Role]]] = None,
                     autorised_key: Optional[Callable] = None) -> SelectMenu` : Set a callable for menus associated with custom_ids. This callable _(async function)_ will be set to respond at selected menus interactions. _data_ parameter is a dict fill with any values to pass in _(async function)_ parameters
> 
> > **Method** `send(target: Union[Member, TextChannel]) -> Any` : Send the selectmenu in dm member or channels
> 
> > **Method** `respond(ctx: Union[ApplicationContext, Interaction]) -> Any` : Respond at slash command call and Interaction
> 
> > **Method** `update() -> None` : Update the view dynamically if there was sent before. 
> 
> > **@Method** `get_callable(self, custom_id: str) -> Union[Callable, None]` : Get the callable _async_ function link to the custom_id ui. If any callable set, return None
> 
> > **@property** `get_view -> EasyModifiedViews` : Return the selectmenu view. Can be used in `view` parameter to setup a view

### Menu

## `Menu`
> ```python
> Menu(...)` # Not to be initialized by the user
> ```
> > **Method** `set_callable(_callable: Union[Callable, None],
                     data: Optional[dict[str, Any]] = None,
                     autorised_roles : Optional[list[Union[int, Role]]] = None,
                     autorised_key: Optional[Callable] = None) -> Menu` : Set a callable for menus associated. This callable _(async function)_ will be set to respond at selected menus interactions
> 
> > **Method** `add_option(label: str, value: str = MISSING, description: Union[str, None] = None, emoji: Union[str, Emoji, PartialEmoji, None] = None, default: bool = False) -> Menu` : Add a string select option. Only for string select menu !
> 
> > **Method** `remove_options(*labels: str) -> Menu` : Remove options with labels. Only for string select menu !
> 
> > **Method** `update_option(current_label: str, new_label: str = None, value: str = None, description: Union[str, None] = None, emoji: Union[str, Emoji, PartialEmoji, None] = None, default: Union[bool, None] = None) -> Menu` : Update option associated with `current_label` parameter
> 
> > **@property** `component -> CustomSelect` : Return the Select component class
> 
> > **@property** `selectmenu -> SelectMenu` : Return the current SelectMenu instance associated
> 
> > **@property** `callable -> Callable` : Return the current callable menu

```python
from pycordViews.menu import SelectMenu
import discord

intents = discord.Intents.all()
bot = discord.AutoShardedBot(intents=intents)

@bot.command(name="My command select")
async def select_command(ctx):
    """
    Create a command select
    """
    async def your_response(select, interaction):
        await interaction.response.send(f"You have selected {select.values[0]} !")
    
    my_selector = SelectMenu(timeout=None, disabled_on_timeout=False) # A basic selector menu
    my_menu = my_selector.add_string_select_menu(placeholder="Choice anything !") # add string_select UI
    
    my_menu.add_option(label="My first choice !", emoji="😊", default=True, description="It's the first choice !", value='first choice')
    my_menu.add_option(label="My second choice !", value='second choice')
    my_menu.set_callable(your_response)
    
    await my_selector.respond(ctx)
    
bot.run("Your token")
```

# Multibot
The Multibot instance is used to manage several bots dynamically.

Each instance of this class creates a process where bots can be added. These bots will each be launched in a different thread with their own asyncio loop.

## `Multibot`
> ```python
> Multibot(global_timeout: int = 30) # global_timeout is the time in seconds the program waits before abandoning the request
> ```
> > **Method** `add_bot(bot_name: str, token: str, intents: Intents) -> None` : Add a bot. The name given here is not the real bot name, it's juste an ID
> 
> > **Method** `remove_bot(bot_name: str) -> dict[str, str]` : Remove à bot. If the bot is online, it will turn off properly. It can take a long time !
> 
> > **Method** `start(*bot_names: str) -> list[dict[str, str]]` : Start bots
> 
> > **Method** `stop(*bot_names: str) -> list[dict[str, str]]` : Stop bots properly
> 
> > **Method** `restart(*bot_names: str) -> list[dict[str, str]]` : Restarts bots
> 
> > **Method** `start_all() -> list[dict[str, list[str]]]` : Start all bot in the process
> 
> > **Method** `stop_all() -> list[dict[str, list[str]]]` : Stop all bot in the process properly
> 
> > **Method** `is_started(bot_name: str) -> bool` : Return if the bot is connected at the Discord WebSocket
> 
> > **Method** `is_ready(bot_name: str) -> bool` : Return if the bot is ready in Discord
> 
> > **Method** `is_ws_ratelimited(bot_name: str) -> bool` : Return if the bot is rate limited by Discord
> 
> > **Method** `reload_commands(*bot_names: str) -> list[dict[str, str]]` : Reload all commands for each bot passed in parameters
> 
> > **Method** `add_pyFile_commands(bot_name: str, file: str, setup_function: str = 'setup', reload_command: bool = True) -> dict[str, str]` : Add a python Discord command file to the bot. `file` parameter require a file path, absolute or not. By default, it automatically reloads commands on the bot after adding the file.
> >
> > ### _Blob_commands.py_
> > ```python
> > """ 
> > Discord command file example. Follow it !
> > This file doesn't have 'bot.run()' function. It's managed by Multibot instance.
> > """
> > 
> > from discord import Bot, ApplicationContext, Message # autoaticly imported by importlib module
> > 
> > # this function is called when the bot load a python file command. It is mandatory to have it with a bot parameter !
> > def setup(bot: Bot):
> >     """
> >     Function called by the process and give the bot instance.
> >     This function is mandatory to have it with a bot parameter but can be renamed with 'setup_function' parameter in 'add_pyFile_commands' method.
> >     Every discord command and discord event can be in this function, but you can make function and class outside setup function.
> >     -> bot : Instance of your started bot.
> >     """
> >     @bot.command()
> >     async def my_first_command(ctx: ApplicationContext):
> >         await ctx.respond("It's my first command !")
> > 
> >     @bot.event
> >     async def on_message(message: Message):
> >         await message.add_reaction(emoji="😊")
> > 
> > # You don't need 'bot.run(...)' here !
> > ```
> 
> > **Method** `modify_pyFile_commands(bot_name: str, file: str, setup_function: str = 'setup') -> dict[str, str]` : Modify python discord command file and setup function. This method doesn't reload automatically commands on the bot. Use `reload_commands` after. `file` parameter require a file path, absolute or not.
> 
> > **@property** `bot_count -> int` : Return the total number of bots
> 
> > **@property** `started_bot_count -> int` : Return the total number of started bots
> 
> > **@property** `shutdown_bot_count( -> int` : Return the total number of shutdown bots
> 
> > **@property** `get_bots_name -> list[str]` : Return all bots name _(not real name of bots)_
```python
from pycordViews.multibot import Multibot
from discord import Intents

if __name__ == '__main__': # Obligatory !
    process = Multibot()
    
    process.add_bot(bot_name="Blob", token="TOKEN FIRST BOT", intents=Intents.all())
    process.add_bot(bot_name="Bee", token="TOKEN SECOND BOT", intents=Intents.all())
    
    process.start_all()
    process.add_pyFile_commands(bot_name='Blob', file='Blob_commands.py', reload_command=True)
    process.add_pyFile_commands(bot_name='Bee', file='Bee_commandes.py', reload_command=True)

    process.modify_pyFile_commands(bot_name='Blob', file='others_commands/Blob2_commands.py', setup_function='started_bot')
    process.reload_commands('Blob')
```