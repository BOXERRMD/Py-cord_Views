from discord import Bot
from discord.ui import Button
from pycordViews import EasyModal

def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        p = EasyModal(title="cc")
        p.add_input_text(label='test', placeholder='HELLOOOOOOOOOO')(test)

        await ctx.respon

        p.wait()

    async def test(data, interaction):
        print(data.value)
