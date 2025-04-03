from multiprocessing import Process, get_context
from multiprocessing.queues import Queue
from .process import ManageProcess
from discord import Intents
from sys import platform


class Multibot:

    def __init__(self):
        """
        Get instance to run few Discord bot
        """
        if platform == 'win32':
            ctx = get_context("spawn")
        else:
            ctx = get_context("forkserver")
        self.main_queue: Queue = ctx.Queue()
        self.process_queue: Queue = ctx.Queue()
        # Création du processus gérant les bots
        self.DiscordProcess = ctx.Process(target=self.start_process)
        self.DiscordProcess.start()

    def start_process(self):
        """
        Initialise et exécute le gestionnaire de processus.
        """
        manager = ManageProcess(self.main_queue, self.process_queue)
        manager.run()

    def add_bot(self, name: str, token: str, intents: Intents):
        """
        Add a bot in the process
        :param name: Bot name
        :param token: Token bot
        :param intents: Intents bot to Intents discord class
        """
        self.main_queue.put({"type": "ADD", "name": name, "token": token, 'intents': intents})
        response = self.process_queue.get()
        return response  # Retourne le statut de l'ajout

    def remove_bot(self, name: str):
        """
        Shutdown and remove à bot
        :param name: Bot name to remove
        """
        self.main_queue.put({"type": "REMOVE", "name": name})
        response = self.process_queue.get(timeout=30)
        return response  # Retourne le statut de la suppression

    def start(self, name: str) -> dict[str, str]:
        """
        Start a single bot
        :param name: Bot name to start
        :return: Data status dict
        """
        self.main_queue.put({'type': "START", 'name': name})
        response = self.process_queue.get(timeout=30)
        return response

    def stop(self, name: str) -> dict[str, str]:
        """
        Stop a single bot
        :param name: Bot name to start
        :return: Data status dict
        """
        self.main_queue.put({'type': "STOP", 'name': name})
        response = self.process_queue.get(timeout=30)
        return response
