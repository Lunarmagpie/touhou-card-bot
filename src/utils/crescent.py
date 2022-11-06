import typing as t

import crescent

import db


class Bot(crescent.Bot):
    def __init__(self, *args: t.Any, **kwargs: t.Any):
        self.db = db.JsonConn()

        super().__init__(*args, **kwargs)


class Context(crescent.Context):
    app: Bot


class Plugin(crescent.Plugin):
    @property
    def app(self) -> Bot:
        return super().app  # type: ignore
