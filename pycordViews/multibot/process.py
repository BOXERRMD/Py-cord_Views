from multiprocessing import Queue
from .errors import BotAlreadyExistError, BotNotFoundError
from .bot import DiscordBot

class ManageProcess:

    def __init__(self, main_queue: Queue, process_queue: Queue):
        """
        Gère tous les bots dans un processus
        """
        self.__bots: dict[str, DiscordBot] = {}

    def add_bot_to_process(self, name: str, token: str):
        """
        Ajoute un bot au processus
        :param name: Le nom du bot
        :param token: Le token du bot
        :raise: BotAlreadyExistError si le bot existe déjà
        """
        if name in self.__bots.keys():
            raise BotAlreadyExistError(name)
        self.__bots[name] = DiscordBot(token)

    def remove_bot_to_process(self, name: str):
        """
        Coupe et enlève un bot au processus
        :param name: Le nom du bot à retirer
        :raise:
        """
        if name not in self.__bots.keys():
            raise BotNotFoundError(name)
        self.__bots[name].stop()
        del self.__bots[name]
        