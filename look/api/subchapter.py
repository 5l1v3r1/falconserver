from look.model.subchapter import Subchapter
from look.api.base import BaseCollection, BaseItem

args = (Subchapter,)

class Collection(BaseCollection):
    def __init__(self):
        super().__init__(*args)

class Item(BaseItem):
    def __init__(self):
        super().__init__(*args)