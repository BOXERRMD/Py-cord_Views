from threading import Thread
from discord import AutoShardedBot, Intents
from asyncio import run_coroutine_threadsafe, new_event_loop, set_event_loop, Future, AbstractEventLoop, create_task

class DiscordBot:

    def __init__(self, token: str, intents: Intents):
        self.__token: str = token
        self.bot: AutoShardedBot = AutoShardedBot(intents=intents)
        self.running_bot: Future = None
        self.loop: AbstractEventLoop = new_event_loop()
        self.thread: Thread = Thread(target=self.run_loop, daemon=True)  # Thread pour exécuter l'event loop
        self.thread.start()

    def run_loop(self):
        """Lance la boucle asyncio dans un thread séparé."""
        set_event_loop(self.loop)
        self.loop.run_forever()

    def start(self) -> None:
        """Démarre le bot"""
        print('bot start')
        self.running_bot = run_coroutine_threadsafe(self.bot.start(token=self.__token, reconnect=True), self.loop)

    def stop(self) -> None:
        """Stop le bot"""
        run_coroutine_threadsafe(self.bot.close(), self.loop)
        print("ok")

    @property
    def is_running(self) -> bool:
        """Renvoie si le bot est actif"""
        return not self.bot.is_closed()
