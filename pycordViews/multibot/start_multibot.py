
from typing import Union, Any
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from asyncio import create_task, sleep, Event

from .process_for_bots import ProcessBot
from .process_messages import ProcessMessage


class Multibot:

    def __init__(self, limit_bots_in_tread: int = 10):
        """
        Create an instance of Multibot_asyncio class to manage few bots with asyncio.
        :param limit_bots_in_tread: Max running bot in a single asyncio loop in a thread.
        """
        self.__parent, self.__children = Pipe()

        self.__process: Union[Process] = Process(target=ProcessBot, args=(self.__children, limit_bots_in_tread))  # Process to run all bots

    async def start_process(self) -> "Multibot":
        """
        Start the process. It is required !
        """
        create_task(self.__message_process_receiver())
        self.__process.start()

    def __message_process_sender(self, message: dict):
        """
        Send a message to children process
        """
        self.__parent: Connection
        self.__parent.send(message)

    async def __message_process_receiver(self):
        """
        Wait message from children process (always a dict with the key "children_message")
        """
        while True:
            if self.__parent.poll():
                message = self.__parent.recv()
                await self.__decode_message(message)
            else:
                await sleep(0.1)

    async def __decode_message(self, message: Any):
        """
        Decode the current message sent by the parent process
        :param message: The message.
        """
        print(message)

    async def add_bot(self, token: str, name: str = None, autoshared: bool = False, **kwargs):
        """
        Add a bot
        """
        data = {
         'parent_message': ProcessMessage.ADD_BOT.value,
         'token': token,
         'name': name,
         'autoshared': autoshared,
         }
        data.update(kwargs)

        self.__message_process_sender(data)

    async def run_all_bots(self):
        """
        Run all bots
        """
        self.__message_process_sender({'parent_message': ProcessMessage.RUN_ALL.value})

        while True:
            await sleep(1)
