from __future__ import annotations

import typing as t

import crescent

from utils.config import CONFIG

if t.TYPE_CHECKING:
    import db


class Bot(crescent.Bot):
    def __init__(self) -> None:

        self._db: db.Database | None = None

        super().__init__(CONFIG.token)

    @property
    def db(self) -> db.Database:
        assert self._db
        return self._db


class Context(crescent.Context):
    app: Bot


class Plugin(crescent.Plugin):
    @property
    def app(self) -> Bot:
        return super().app  # type: ignore
