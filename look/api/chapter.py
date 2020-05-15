from look.model.chapter import Chapter
from look.api.base import BaseCollection, BaseItem

args = (Chapter,)

class Collection(BaseCollection):
    def __init__(self):
        super().__init__(*args)

class Item(BaseItem):
    def __init__(self):
        super().__init__(*args)