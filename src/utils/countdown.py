import time

def countdown(countdown_time: int) -> str:
    return f"<t:{time.time() + countdown_time}:R>"