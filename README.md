# Py-cord_Views
 Views for py-cord library

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
    await pages.send(send_to=ctx.author) # send the message to the command author
```