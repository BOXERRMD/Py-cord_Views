from multiprocessing import Queue
from .errors import BotAlreadyExistError, BotNotFoundError, MultibotError, BotNotStartedError
from .bot import DiscordBot
from discord import Intents
from textwrap import dedent

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
            "BOTS_NAME": self.get_bots_name,
            "ADD_COMMAND": self.add_command,
            "RELOAD_COMMANDS": self.reload_all_commands
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

    def add_command(self, name: str, func_name: str, source_code: str):
        """
        Ajoute une commande dynamiquement au bot
        """
        self.if_bot_no_exist(name)
        local_vars = {}
        exec(dedent(''.join(source_code.splitlines(keepends=True)[1:])), globals(), local_vars)
        command_func = local_vars[func_name]
        self.__bots[name].add_command(command_func)

        return f"Command '{func_name}' added to bot '{name}'"

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

    def reload_all_commands(self, name: str):
        """
        Recharge toutes les commandes sur Discord
        """
        self.if_bot_no_exist(name)
        self.__bots[name].reload_commands()
        return f'Bot {name} commands reloaded'

    def remove_bot_to_process(self, name: str) -> str:
        """
        Coupe et enlève un bot au processus
        :param name: Le nom du bot à retirer
        :raise:
        """
        self.if_bot_no_exist(name)
        try:
            self.__bots[name].stop()
        except BotNotStartedError:
            pass
        del self.__bots[name]
        return f'Bot {name} removed'

    def is_started(self, name: str) -> bool:
        """
        Regarde si la connexion au Websocket est effectué
        :param name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(name)
        return self.__bots[name].is_running

    def is_ready(self, name: str) -> bool:
        """
        Regarde si le bot est ready
        :param name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(name)
        return self.__bots[name].is_ready

    def is_ws_ratelimited(self, name: str) -> bool:
        """
        Regarde si le bot est ratelimit
        :param name: Le nom du bot à vérifier
        """
        self.if_bot_no_exist(name)
        return self.__bots[name].is_ws_ratelimited

    def if_bot_no_exist(self, name: str) -> None:
        """
        Regarde si le bot existe dans la class
        """
        if name not in self.__bots.keys():
            raise BotNotFoundError(name)

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

    def get_bots_name(self) -> list[str]:
        """
        Renvoie tous les noms des bots entrée par l'utilisateur
        """
        return list(self.__bots.keys())
