from discord import Bot
from discord.ui import Button
from pycordViews import Pagination

def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        p = Pagination()
        p.add_page(content='coucou')
        p.add_page(content='bye')
        p.get_page(1).get_page_view.add_items(Button(label='Test'))
        p.add_page(content='fff')

        await p.respond(ctx)

