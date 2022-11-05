import contextlib
import typing as t
import asyncio

T = t.TypeVar("T")
Self = t.TypeVar("Self", bound="TaskGroup")


class TaskGroup(contextlib.AbstractAsyncContextManager):
    def __init__(self) -> None:
        self.tasks = []

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(self, *_) -> None:
        await asyncio.gather(*self.tasks)

    def create_task(self, awaitable: t.Awaitable[T]) -> asyncio.Task[T]:
        task = asyncio.create_task(awaitable)
        self.tasks.append(task)
        return task
