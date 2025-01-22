class Py_cordEasyModifiedViews(Exception):
    """
    Main class exception
    """


class CustomIDNotFound(Py_cordEasyModifiedViews):
    def __init__(self):
        super().__init__(f"custom_id not found !")