from discord import Bot


def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        print("Test command executed")
