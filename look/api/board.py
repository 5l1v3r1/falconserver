from look.model.board import Board
from look.api.base import BaseCollection, BaseItem

args = (Board,)

class Collection(BaseCollection):
    def __init__(self):
        super().__init__(*args)

class Item(BaseItem):
    def __init__(self):
        super().__init__(*args)