from discord import AutoShardedBot, Bot
from typing import Union

class Runner:

    def __init__(self, bot: Union[AutoShardedBot, Bot]):
        """
        Run the bot
        """
        self.bot: Union[AutoShardedBot, Bot] = bot

    def __reduce__(self):
        # Renvoyer un tuple avec les informations nécessaires pour reconstruire l'objet
        return self.__class__, (self.bot,)
