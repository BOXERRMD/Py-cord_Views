from discord import AutoShardedBot, Bot
from random import choice
from string import ascii_letters
from asyncio import set_event_loop, new_event_loop, sleep, run, create_task
from multiprocessing import Queue

from .errors import *
from .runner import Runner
from .process_messages import ProcessMessage


class ProcessBot:

    def __init__(self, queue_parent: Queue, queue_children: Queue, limit_bots_in_tread: int = -1):
        """
        Class to manage process and thread
        """
        self.__threads: dict = {}
        self.__all_bots: dict = {}

        self.__limit_bots_in_tread: int = limit_bots_in_tread

        self.__queue_parent: Queue = queue_parent
        self.__queue_children: Queue = queue_children
        self.__loop = None
        run(self.run_process())

    async def run_process(self):
        """
        Function run with the process
        """
        await create_task(self.__message_process_receiver())  # Run the process

    async def __message_process_receiver(self):
        """
        Wait message from parent process (always a dict with the key "parent_message")
        """
        while True:
            await sleep(0.02)
            while not self.__queue_children.empty():
                try:
                    message = self.__queue_children.get_nowait()
                    await self.__decode_message(message)
                except:
                    break

    def __message_process_sender(self, message: dict):
        """
        Send a message to parent process
        """
        self.__queue_parent.put(message)

    async def __decode_message(self, message: dict):
        """
        Decode the current message sent by the parent process
        :param message: The message.
        """
        action = message['parent_message']

        if ProcessMessage.ADD_BOT.value == action:
            self.add_bot(**message)

        elif ProcessMessage.RUN_ALL.value == action:
            print("run all bots")

    def add_bot(self, token: str, *args, autoshared: bool = False, name: str = None, **kwargs) -> None:
        """
        Add a bot in the instance to manage it.
        Use this function to set the bot's intents and other subtleties.
        :param name: The name of the bot to find it. If None, a random name is given
        :param token: The token bot
        :param autoshared: Autoshare the bot in Discord
        :param args: all arguments of the Discord class Bot.
        :param kwargs: all kwargs of the Discord class Bot
        See : https://docs.pycord.dev/en/stable/api/clients.html#discord.Bot
        """
        print(f"Ajout du bot {name} avec le token {token}")
        if name is None:
            name = ''.join([choice(ascii_letters) for _ in range(20)])

        if autoshared:
            self.__all_bots[name] = {'runner': Runner(AutoShardedBot(*args, **kwargs)),
                                     'token': token,
                                     'thread': None}

        else:
            self.__all_bots[name] = {'runner': Runner(Bot(*args, **kwargs)),
                                     'token': token,
                                     'thread': None}

        print(f"Envoi de la réponse 'coucou' pour {name}")
        self.__message_process_sender({'children_message': "coucou"})


    def get_bots_names(self) -> list[str]:
        """
        Return all bots names registered in the class.
        """
        print('coucou', self.__event)
        return list(self.__all_bots.keys())


    def get_runner(self, name: str) -> "Runner":
        """
        Run the bot runner associated with this name
        :raise: BotNotFoundError
        """

        if name not in self.__all_bots.keys():
            raise BotNotFoundError(name)

        return self.__all_bots[name]['runner']
