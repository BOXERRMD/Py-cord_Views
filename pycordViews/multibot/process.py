from multiprocessing import Queue
from .errors import BotAlreadyExistError, BotNotFoundError, MultibotError
from .bot import DiscordBot
from discord import Intents

class ManageProcess:

    def __init__(self, main_queue: Queue, process_queue: Queue):
        """
        Gère tous les bots dans un processus
        """
        self.__bots: dict[str, DiscordBot] = {}
        self.main_queue: Queue = main_queue
        self.process_queue: Queue = process_queue

        self.commandes = {
            "ADD": self.add_bot_to_process,
            "REMOVE": self.remove_bot_to_process,
            "START": self.start_bot_to_process,
            "STOP": self.stop_bot_to_process
        }

    def run(self):
        """
        Boucle principale du processus, écoute la queue principale.
        Doit comporter aubligatoirement un dictionnaire avec la clé 'type'
        """
        while True:
            if not self.main_queue.empty():
                command: dict = self.main_queue.get()
                print(command)

                c = command["type"]
                if c in self.commandes.keys():
                    del command['type']
                    try:
                        result = self.commandes[c](**command)
                        self.process_queue.put({'status': 'success', 'message': result})
                    except MultibotError as e:
                        self.process_queue.put({'status': 'error', 'message': e})

    def start_bot_to_process(self, name: str) -> str:
        """
        Lance un unique bot
        """
        self.if_bot_no_exist(name)
        self.__bots[name].start()
        return f'{name} bot started'

    def stop_bot_to_process(self, name: str) -> str:
        """
        Stop un bot du processus
        :param name: Le nom du bot à stopper
        """
        self.if_bot_no_exist(name)
        self.__bots[name].stop()
        return f'{name} bot stopped'

    def add_bot_to_process(self, name: str, token: str, intents: Intents) -> str:
        """
        Ajoute un bot au processus
        :param name: Le nom du bot
        :param token: Le token du bot
        :raise: BotAlreadyExistError si le bot existe déjà
        """
        if name in self.__bots.keys():
            raise BotAlreadyExistError(name)
        self.__bots[name] = DiscordBot(token, intents)
        return f'Bot {name} added'

    def remove_bot_to_process(self, name: str) -> str:
        """
        Coupe et enlève un bot au processus
        :param name: Le nom du bot à retirer
        :raise:
        """
        self.if_bot_no_exist(name)
        self.__bots[name].stop()
        del self.__bots[name]
        return f'Bot {name} removed'

    def if_bot_no_exist(self, name: str) -> None:
        """
        Regarde si le bot existe dans la class
        """
        if name not in self.__bots.keys():
            raise BotNotFoundError(name)
