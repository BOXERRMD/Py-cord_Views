class MultibotError(Exception):
    pass

class BotAlreadyExistError(MultibotError):
    def __init__(self, bot_name: str):
        super().__init__(f"'{bot_name}' bot already exist !")

class BotNotFoundError(MultibotError):
    def __init__(self, bot_name: str):
        super().__init__(f"'{bot_name}' bot doesn't exist !")
