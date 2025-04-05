from threading import Thread
from discord import Intents, Client
from asyncio import run_coroutine_threadsafe, new_event_loop, set_event_loop, Future, AbstractEventLoop, sleep
from .errors import BotNotStartedError

class DiscordBot:

    def __init__(self, token: str, intents: Intents):
        self.__token: str = token
        self.__running_bot: Future = None
        self.__loop: AbstractEventLoop = new_event_loop()
        self.__thread: Thread = Thread(target=self.run_loop, daemon=True)  # Thread pour exécuter l'event loop
        self.__thread.start()
        self.__bot: Client = Client(loop=self.__loop, intents=intents)
        self.__intents: Intents = intents

    def run_loop(self):
        """Lance la boucle asyncio dans un thread séparé."""
        set_event_loop(self.__loop)
        self.__loop.run_forever()

    def start(self) -> None:
        """Démarre le bot"""

        self.__running_bot: Future = run_coroutine_threadsafe(self.__bot.start(token=self.__token, reconnect=True), self.__loop)

    def stop(self) -> None:
        """
        Stop le bot proprement depuis un autre thread
        :raise: BotNotStartedError
        """
        if self.is_running:
            # Attendre que la fermeture du bot soit terminée
            run_coroutine_threadsafe(self.__stop_bot_in_thread(), self.__loop).result(timeout=30)
            self.__bot = Client(token=self.__token, intents=self.__intents)
        else:
            raise BotNotStartedError(self.__bot.user.name)

    @property
    def is_running(self) -> bool:
        """Renvoie si la Websocket est connectée"""
        return not self.__bot.is_closed()

    @property
    def is_ready(self) -> bool:
        """
        Renvoie si le bot est ready
        """
        return self.__bot.is_ready()

    @property
    def is_ws_ratelimited(self) -> bool:
        """
        Renvoie si le bot est rate limit
        """
        return self.__bot.is_ws_ratelimited()


    async def __stop_bot_in_thread(self):
        """
        Clear le cache du bot de manière asynchrone
        """
        await self.__bot.close()

