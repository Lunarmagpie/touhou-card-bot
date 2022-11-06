import asyncio
import contextlib
import typing as t

T = t.TypeVar("T")
Self = t.TypeVar("Self", bound="TaskGroup")


class TaskGroup(contextlib.AbstractAsyncContextManager[t.Any]):
    def __init__(self) -> None:
        self.tasks: list[asyncio.Task[t.Any]] = []

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(self, *_: t.Any) -> None:
        await asyncio.gather(*self.tasks)

    def create_task(self, awaitable: t.Awaitable[T]) -> asyncio.Task[T]:
        task: asyncio.Task[T] = asyncio.create_task(awaitable)  # type: ignore
        self.tasks.append(task)
        return task
