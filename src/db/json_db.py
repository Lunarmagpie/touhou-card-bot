import json
import os

from db.conn import ConnABC
from db.modal import PlayerModal


class JsonConn(ConnABC):
    def __init__(self) -> None:
        self.fp = "db.json"
        if not os.path.exists(self.fp):
            with open(self.fp, "w") as f:
                f.write('{"players":{}}')

    async def fetch_player(self, id: int) -> PlayerModal:
        with open(self.fp, "r") as f:
            json_ = json.load(f)
            if str(id) in json_:
                return PlayerModal(**json_[str(id)])
            else:
                modal = PlayerModal.default()
                json_[str(id)] = modal.to_dict()
                with open(self.fp, "w") as f:
                    json.dump(json_, f)
                return modal

    async def post_player(self, id: int, player: PlayerModal) -> None:
        with open(self.fp, "r") as f:
            json_ = json.load(f)
            json_[str(id)] = player.to_dict()
        with open(self.fp, "w") as f:
            json.dump(json_, f)
