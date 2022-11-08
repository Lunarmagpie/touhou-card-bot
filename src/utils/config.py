import dataclasses

import dotenv


@dataclasses.dataclass
class Config:
    token: str
    db: str
    db_user: str
    db_host: str
    db_password: str


_ENV = dotenv.dotenv_values()

CONFIG = Config(
    token=_ENV["TOKEN"],  # type: ignore
    db=_ENV["DB"],  # type: ignore
    db_user=_ENV["DB_USER"],  # type: ignore
    db_host=_ENV["DB_HOST"],  # type: ignore
    db_password=_ENV["DB_PASSWORD"],  # type: ignore
)
