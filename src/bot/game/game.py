import hikari
import asyncio

from bot.game.discord_game import DiscordGame

import utils
import typing as t


class Game:
    start_game_timeout: t.ClassVar[int] = 30

    def __init__(self, app: utils.Bot, players: tuple[hikari.User, hikari.User]) -> None:
        self.players = players
        self.discord = DiscordGame(app)
        self._wait_for_started_event = asyncio.Event()

    async def wait_until_started(self) -> bool:
        """Wait until the game starts. Return `False` if the game timed out."""
        started = True

        async def second() -> None:
            nonlocal started
            await asyncio.sleep(self.start_game_timeout)
            started = False
            self._wait_for_started_event.set()

        second_task = asyncio.create_task(second())
        await self._wait_for_started_event.wait()
        if started:
            second_task.cancel()

        return started

    async def loop(self) -> None:
        """The main game loop"""

        while True:
            await self._round()

    async def _round(self) -> None:
        from bot.game.round import build_card_buttons

        await self._send_stats()

        await self.discord.respond_to_player(
            0, content="Select your cards:", component=await build_card_buttons(self)
        )
        await self.discord.respond_to_player(
            1, content="Select your cards:", component=await build_card_buttons(self)
        )

        await asyncio.sleep(20)

        await self.discord.delete_responses()


    async def _send_stats(self) -> None:
        await self.discord.respond_global(content="These are some stats.")
