from discord import Intents, Bot
from pycordViews import Poll

def setup(bot):

    @bot.command()
    async def test(ctx):
        p = Poll(timeout=10)
        await ctx.respond(f"Test de poll", view=p.get_view)

