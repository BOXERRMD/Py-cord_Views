class Py_cordViews(Exception):
    """
    Main class exception
    """


class CustomIDNotFound(Py_cordViews):
    def __init__(self):
        super().__init__(f"custom_id not found !")