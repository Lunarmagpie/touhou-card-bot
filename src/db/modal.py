from __future__ import annotations

import dataclasses
import typing as t

import typing_extensions


@typing_extensions.dataclass_transform()
class BaseModal:
    def __init_subclass__(cls) -> None:
        dataclasses.dataclass(kw_only=True)(cls)

    def to_dict(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class PlayerModal(BaseModal):
    decks: dict[int, list[int]]

    @classmethod
    def default(cls) -> PlayerModal:
        return cls(decks={})
