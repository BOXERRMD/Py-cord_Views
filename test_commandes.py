from discord import Bot
from discord.ui import Button
from pycordViews import EasyModifiedViews

def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        p = EasyModifiedViews()
        p.add_items(Button(label='coucou', custom_id='1234'))
        p.set_callable('1234', _callable=test)
        await ctx.respond(view=p, content='coucou !')

    async def test(ui, interaction, data):
        await interaction.respond('ok')
