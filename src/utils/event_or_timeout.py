import asyncio


async def event_or_timout(timeout: int, *events: asyncio.Event) -> bool:
    """Return `True` if there was a timeout."""
    timed_out = False

    async def second() -> None:
        nonlocal timed_out
        await asyncio.sleep(timeout)
        timed_out = True

        for event in events:
            event.set()

    timer_task = asyncio.create_task(second())

    async def wait_for_event(event: asyncio.Event) -> None:
        await event.wait()

    await asyncio.gather(*(wait_for_event(e) for e in events))

    if timed_out:
        timer_task.cancel()

    return timed_out
