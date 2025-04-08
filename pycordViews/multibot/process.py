from multiprocessing import Queue
from .errors import BotAlreadyExistError, BotNotFoundError, MultibotError, BotNotStartedError
from .bot import DiscordBot
from discord import Intents
from immutableType import Str_

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
            "STOP": self.stop_bot_to_process,
            "IS_STARTED": self.is_started,
            "IS_READY": self.is_ready,
            "IS_WS_RATELIMITED": self.is_ws_ratelimited,
            "STOPALL": self.stop_all_bot_to_process,
            "STARTALL": self.start_all_bot_to_process,
            "BOT_COUNT": self.bot_count,
            "STARTED_BOT_COUNT": self.started_bot_count,
            "SHUTDOWN_BOT_COUNT": self.shutdown_bot_count,
            "BOTS_bot_name": self.get_bots_bot_name,
            "RELOAD_COMMANDS": self.reload_all_commands,
            "ADD_COMMAND_FILE": self.add_pyFile_commands,
            "MODIFY_COMMAND_FILE": self.modify_pyFile_commands
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

    def start_bot_to_process(self, bot_name: str) -> str:
        """
        Lance un unique bot
        """
        self.if_bot_no_exist(bot_name)
        self.__bots[bot_name].start()
        return f'{bot_name} bot started'

    def stop_bot_to_process(self, bot_name: str) -> str:
        """
        Stop un bot du processus
        :param bot_name: Le nom du bot à stopper
        """
        self.if_bot_no_exist(bot_name)
        self.__bots[bot_name].stop()
        return f'{bot_name} bot stopped'

    def start_all_bot_to_process(self) -> list[str]:
        """
        Start tous les bots du processus
        """
        result = []
        for bot in self.__bots.keys():
            result.append(self.start_bot_to_process(bot))
        return result

    def stop_all_bot_to_process(self) -> list[str]:
        """
        Stop tous les bots du processus
        """
        result = []
        for bot in self.__bots.keys():
            result.append(self.stop_bot_to_process(bot))

        return result

    def add_bot_to_process(self, bot_name: str, token: str, intents: Intents) -> str:
        """
        Ajoute un bot au processus
        :param bot_name: Le nom du bot
        :param token: Le token du bot
        :raise: BotAlreadyExistError si le bot existe déjà
        """
        if bot_name in self.__bots.keys():
            raise BotAlreadyExistError(bot_name)
        self.__bots[bot_name] = DiscordBot(token, intents)
        return f'Bot {bot_name} added'

    def add_pyFile_commands(self, bot_bot_name: str, file: str, setup_function: str, reload_command: bool):
        """
        Ajoute et charge un fichier de commande bot et ses dépendances.
        Les fichiers doivent avoir une fonction appelée « setup » ou un équivalent passé en paramètre.

        def setup(bot: Bot) :
            ...

        :param bot_bot_name : Le nom du bot à ajouter au fichier de commandes
        :param file: Chemin relatif ou absolue du fichier de commande
        :param setup_function : Nom de la fonction appelée par le processus pour donner l'instance de Bot.
        :param reload_command : Recharge toutes les commandes dans le fichier et les dépendances. Défaut : True
        """
        self.if_bot_no_exist(bot_bot_name)
        setup_function = Str_(setup_function).str_
        file = Str_(file).str_
        self.__bots[bot_bot_name].add_pyFile_commands(file=file, setup_function=setup_function, reload_command=reload_command)

    def modify_pyFile_commands(self, bot_bot_name: str, file: str, setup_function: str):
        """
        Modifie un fichier de comandes et le recharge.
        Ne recharge que le fichier et non les commandes du bot !
        :param bot_bot_name: Le nom du bot
        :param file: Le chemin d'accès relatif ou absolue du fichier
        """
        self.if_bot_no_exist(bot_bot_name)
        file = Str_(file).str_
        self.__bots[bot_bot_name].modify_pyFile_commands(file=file, setup_function=setup_function)


    def reload_all_commands(self, bot_name: str):
        """
        Recharge toutes les commandes sur Discord
        """
        self.if_bot_no_exist(bot_name)
        self.__bots[bot_name].reload_commands()
        return f'Bot {bot_name} commands reloaded'

    def remove_bot_to_process(self, bot_name: str) -> str:
        """
        Coupe et enlève un bot au processus
        :param bot_name: Le nom du bot à retirer
        :raise:
        """
        self.if_bot_no_exist(bot_name)
        try:
            self.__bots[bot_name].stop()
        except BotNotStartedError:
            pass
        self.__bots[bot_name].close_ascyncio_loop()
        del self.__bots[bot_name]
        return f'Bot {bot_name} removed'

    def is_started(self, bot_name: str) -> bool:
        """
        Regarde si la connexion au Websocket est effectué
        :param bot_name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(bot_name)
        return self.__bots[bot_name].is_running

    def is_ready(self, bot_name: str) -> bool:
        """
        Regarde si le bot est ready
        :param bot_name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(bot_name)
        return self.__bots[bot_name].is_ready

    def is_ws_ratelimited(self, bot_name: str) -> bool:
        """
        Regarde si le bot est ratelimit
        :param bot_name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(bot_name)
        return self.__bots[bot_name].is_ws_ratelimited

    def if_bot_no_exist(self, bot_name: str) -> None:
        """
        Regarde si le bot existe dans la class
        """
        if bot_name not in self.__bots.keys():
            raise BotNotFoundError(bot_name)

    def bot_count(self) -> int:
        """
        Renvoie le nombre de bot au total
        """
        return len(self.__bots)

    def started_bot_count(self) -> int:
        """
        Renvoie le nombre de bot démarré au total
        """
        s = 0
        for bot in self.__bots.values():
            if bot.is_running:
                s += 1
        return s

    def shutdown_bot_count(self) -> int:
        """
        Renvoie le nombre de bot arrêter au total
        """
        s = 0
        for bot in self.__bots.values():
            if not bot.is_running:
                s += 1
        return s

    def get_bots_bot_name(self) -> list[str]:
        """
        Renvoie tous les noms des bots entrée par l'utilisateur
        """
        return list(self.__bots.keys())
