from multiprocessing import Process, get_context
from multiprocessing.queues import Queue
from .process import ManageProcess
from discord import Intents
from sys import platform


class Multibot:

    def __init__(self, global_timeout: int = 30):
        """
        Get instance to run few Discord bot
        """
        if platform == 'win32':
            ctx = get_context("spawn")
        else:
            ctx = get_context("forkserver")
        self.__main_queue: Queue = ctx.Queue()
        self.__process_queue: Queue = ctx.Queue()
        # Création du processus gérant les bots
        self.__DiscordProcess = ctx.Process(target=self._start_process)
        self.__DiscordProcess.start()
        
        self.global_timeout = global_timeout

    def _start_process(self):
        """
        Initialise et exécute le gestionnaire de processus.
        """
        manager = ManageProcess(self.__main_queue, self.__process_queue)
        manager.run()

    def add_bot(self, name: str, token: str, intents: Intents):
        """
        Add a bot in the process
        :param name: Bot name
        :param token: Token bot
        :param intents: Intents bot to Intents discord class
        """
        self.__main_queue.put({"type": "ADD", "name": name, "token": token, 'intents': intents})
        response = self.__process_queue.get()
        return response  # Retourne le statut de l'ajout

    def remove_bot(self, name: str) -> dict[str, str]:
        """
        Shutdown and remove à bot
        :param name: Bot name to remove
        """
        self.__main_queue.put({"type": "REMOVE", "name": name})
        response = self.__process_queue.get(timeout=self.global_timeout)
        return response  # Retourne le statut de la suppression

    def start(self, *names: str) -> list[dict[str, str]]:
        """
        Start bots
        :param names: Bots name to start
        :return: List of data bot status
        """
        results = []
        for bot_name in names:
            self.__main_queue.put({'type': "START", 'name': bot_name})
            results.append(self.__process_queue.get(timeout=self.global_timeout))
        return results

    def stop(self, *names: str) -> list[dict[str, str]]:
        """
        Stop bots
        :param name: Bots name to start
        :return: Data status dict
        """
        results = []
        for bot_name in names:
            self.__main_queue.put({'type': "STOP", 'name': bot_name})
            results.append(self.__process_queue.get(timeout=self.global_timeout))
        return results
    
    def start_all(self) -> list[dict[str, list[str]]]:
        """
        Start all bots in the process.
        """
        self.__main_queue.put({'type': "STARTALL"})
        return self.__process_queue.get(timeout=self.global_timeout)
    
    def stop_all(self) -> list[dict[str, list[str]]]:
        """
        Stop all bots in the process.
        This function is slow ! It's shutdown all bots properly.
        """
        self.__main_queue.put({'type': "STOPALL"})
        return self.__process_queue.get(timeout=self.global_timeout)

    def is_started(self, name: str) -> bool:
        """
        Return the current Websocket connexion status
        :param name: Bot name
        :return: True if the Websocket is online, else False
        """
        self.__main_queue.put({'type': "IS_STARTED", 'name': name})
        return self.__process_queue.get(timeout=self.global_timeout)['message']

    def is_ready(self, name: str) -> bool:
        """
        Return the current bot connexion status
        :param name: Bot name
        :return: True if the bot if ready, else False
        """
        self.__main_queue.put({'type': "IS_READY", 'name': name})
        return self.__process_queue.get(timeout=self.global_timeout)['message']

    def is_ws_ratelimited(self, name: str) -> bool:
        """
        Get the current ratelimit status of the bot
        :param name: Bot name
        :return: True if the bot was ratelimited, else False
        """
        self.__main_queue.put({'type': "IS_WS_RATELIMITED", 'name': name})
        return self.__process_queue.get(timeout=self.global_timeout)['message']

    @property
    def bot_count(self) -> int:
        """
        Return the total number of bots
        """
        self.__main_queue.put({'type': "BOT_COUNT"})
        return self.__process_queue.get(timeout=self.global_timeout)['message']

    @property
    def started_bot_count(self) -> int:
        """
        Return the total number of started bots
        """
        self.__main_queue.put({'type': "STARTED_BOT_COUNT"})
        return self.__process_queue.get(timeout=self.global_timeout)['message']

    @property
    def shutdown_bot_count(self) -> int:
        """
        Return the total number of shutdown bots
        """
        self.__main_queue.put({'type': "SHUTDOWN_BOT_COUNT"})
        return self.__process_queue.get(timeout=self.global_timeout)['message']
