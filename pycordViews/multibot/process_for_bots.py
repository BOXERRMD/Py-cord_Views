from discord import AutoShardedBot, Bot
from random import choice
from string import ascii_letters
from asyncio import set_event_loop, new_event_loop, get_event_loop, Event

from .errors import *
from .runner import Runner


class ProcessBot:

    def __init__(self):
        """
        Class to manage process and thread
        """
        self.__threads: dict = {}
        self.__all_bots: dict = {}

        self.__limit_bots_in_tread: int = -1

        self.__event: Event = None


    def run_process(self, limit_bots_in_tread: int):
        """
        Function run with the process
        """
        self.__limit_bots_in_tread = limit_bots_in_tread
        print(self.__limit_bots_in_tread)

        loop = new_event_loop()
        set_event_loop(loop)

        self.__event = Event()

        loop.create_task(self.main_loop())

        loop.run_forever()


    async def main_loop(self):
        """

        """
        await self.__event.wait()
        print("ok")
        self.__event.clear()


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
