import apgorm

from db import modal


class Database(apgorm.Database):
    players = modal.PlayerModel
