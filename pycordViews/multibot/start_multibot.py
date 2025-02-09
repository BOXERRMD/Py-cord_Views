
from typing import Union
from multiprocessing import Process
from time import sleep

from .process_for_bots import ProcessBot


class Multibot:

    def __init__(self, limit_bots_in_tread: int = 10):
        """
        Create an instance of Multibot_asyncio class to manage few bots with asyncio.
        :param limit_bots_in_tread: Max running bot in a single asyncio loop in a thread.
        """
        self.__processbot = ProcessBot()
        self.__process: Union[Process] = Process(target=self.__processbot.run_process, args=(limit_bots_in_tread, ))  # Process to run all bots

    def start_process(self) -> "Multibot":
        """
        Start the process. It is required !
        """
        self.__process.start()
        return self

    @property
    def bots(self) -> ProcessBot:
        """
        Get the process to manage all bots
        """
        return self.__processbot
