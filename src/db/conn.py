import abc

from db.modal import PlayerModal


class ConnABC:
    @abc.abstractmethod
    async def fetch_player(self, id: int) -> PlayerModal:
        ...

    @abc.abstractmethod
    async def post_player(self, id: int, player: PlayerModal) -> None:
        ...
