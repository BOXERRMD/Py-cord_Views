class Py_cordViews(Exception):
    """
    Main class exception
    """


class CustomIdRequired(Py_cordViews):
    def __init__(self):
        super().__init__(f"custom_id is required in a UI !")

class CustomIDNotFound(Py_cordViews):
    def __init__(self):
        super().__init__(f"custom_id not found !")