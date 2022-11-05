import math
import time
import typing as t

__all__: t.Sequence[str] = ("countdown",)


def countdown(countdown_time: int) -> str:
    return f"<t:{math.floor(time.time() + countdown_time)}:R>"
