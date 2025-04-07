from discord import Bot



def setup(bot):
    @bot.command()
    async def test(ctx):
        await ctx.respond('zzz!')