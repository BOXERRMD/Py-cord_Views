from multiprocessing import Process
from multiprocessing.queues import Queue
from .process import ManageProcess


class Multibot:

    def __init__(self):
        """
        Get instance to run few Discord bot
        """
        self.main_queue: Queue = Queue()
        self.process_queue: Queue = Queue()
        self.DiscordProcess = Process(target=ManageProcess, args=(self.main_queue, self.process_queue))

    def add_bot(self, name: str, token: str):
        """
        Add a bot in the process
        :param name: Bot name
        :param token: Token bot
        """
        if name in self.__bots.keys():
            raise ValueError(f"'{name}' bot already existing !")

        self.__bots[name] = DiscordBot(token)

    def remove_bot(self, name: str):
        """
        Shutdown and remove à bot
        :param name: Bot name to remove
        """
        if name not in self.__bots.keys():
            raise ValueError(f"'{name}' bot doesn't exist !")
        self.__bots[name].stop()