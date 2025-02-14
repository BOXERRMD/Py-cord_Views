# Py-cord_Views
 Views for py-cord library

```python
from pycordViews.pagination import Pagination
from pycordViews.menu import SelectMenu
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
    await pages.send(send_to=ctx.author) # send the message to the command author
    
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