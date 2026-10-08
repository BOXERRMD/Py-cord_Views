from discord import Bot, InputText
from pycordViews import EasyModal

async def callback_function(ui: InputText, interaction):
    await interaction.response.send_message(f"You entered: {ui.value}", ephemeral=True)


def setup(bot: Bot):

    @bot.command()
    async def test(ctx):
        modal = EasyModal(title="Test Modal")
        modal.add_input_text(label="Enter something", placeholder="Type here...", required=True)(callback_function)
        await ctx.send_modal(modal)

