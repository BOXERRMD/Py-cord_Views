
from typing import Union, Any
from multiprocessing import Process, Queue, set_start_method, get_start_method
from asyncio import create_task, sleep
from time import sleep as tsleep

from .process_for_bots import ProcessBot
from .process_messages import ProcessMessage


class Multibot:

    def __init__(self, limit_bots_in_tread: int = 10):
        """
        Create an instance of Multibot_asyncio class to manage few bots with asyncio.
        :param limit_bots_in_tread: Max running bot in a single asyncio loop in a thread.
        """
        if get_start_method() != "spawn":
            set_start_method("spawn")

        self.__queue_parent: Queue = Queue()
        self.__queue_children: Queue = Queue()

        self.__process: Union[Process] = Process(target=ProcessBot, args=(self.__queue_parent, self.__queue_children, limit_bots_in_tread))  # Process to run all bots

    async def start_process(self) -> "Multibot":
        """
        Start the process. It is required !
        """
        self.__process.start()
        create_task(self.__message_process_receiver())

    def __message_process_sender(self, message: dict):
        """
        Send a message to children process
        """
        print(f"Message envoyé par le parent : {message}")
        self.__queue_children.put(message)

    async def __message_process_receiver(self):
        """
        Wait message from children process (always a dict with the key "children_message")
        """
        while True:
            await sleep(0.02)
            while not self.__queue_parent.empty():
                try:
                    message = self.__queue_parent.get_nowait()
                    await self.__decode_message(message)
                except:
                    break

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


