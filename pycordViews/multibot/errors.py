class MultibotError(Exception):
    pass


class BotNotFoundError(MultibotError):
    """
    If the bot is not found with the given name
    """
    def __init__(self, name: str):
        super().__init__(f"{name} is not found")