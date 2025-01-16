from discord.ui import View, Item

from py_cordViews.typeViews import T_views


_DATA_VIEWS: dict[str, list] = {}

class EasyModifiedViews(View):
    """
    Class
    -------------
    Allows you to easily modify and replace an ui.
    """

    def __init__(self, vid: str, timeout=None, *items: Item):
        super().__init__(*items, timeout=timeout)

    def add_view(self,
                   *views: T_views):
        pass

"""
Créer un décorateur permettant de choisisr une fonction asynchrone pour chaque ui d'une instance de la class EasyModifiedViews.
Pour savoir à quelle instance de la class l'ui appartient, il faudra renseigner le "vid" (view ID) unique de l'instance et le "custom_id" de l'ui en question qui doit-être dans la class.
"""

