from discord import Bot
from pycordViews import Confirm

def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        p = Confirm(timeout=10)
        await ctx.respond(f"Test de poll", view=p.get_view)
        result = await p.wait_for_response()
        await ctx.send(content=str(result))

