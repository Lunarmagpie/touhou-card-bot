import dataclasses
import dotenv


@dataclasses.dataclass
class Config:
    token: str


_ENV = dotenv.dotenv_values()

CONFIG = Config(token=_ENV["TOKEN"])  # type: ignore
