from look.model.category import Category
from look.api.base import BaseCollection, BaseItem

args = (Category,)

class Collection(BaseCollection):
    def __init__(self):
        super().__init__(*args)

class Item(BaseItem):
    def __init__(self):
        super().__init__(*args)