from look.model.user import User
from look.api.base import BaseCollection, BaseItem

# args = (User,)
args = (User, 'id', 'username', 'email', 'exp', 'user_img', 'learning_progress')

class Collection(BaseCollection):
    def __init__(self):
        super().__init__(*args)

class Item(BaseItem):
    def __init__(self):
        super().__init__(*args)