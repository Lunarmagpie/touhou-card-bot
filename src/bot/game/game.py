import hikari
import asyncio

from bot.game.discord_game import DiscordGame
from bot.game.player import Player
import time
import utils
import typing as t


class Game:
    start_game_timeout: t.ClassVar[int] = 30

    def __init__(self, app: utils.Bot, players: tuple[hikari.User, hikari.User]) -> None:
        self.players = (Player(players[0]), Player(players[1]))
        self.discord = DiscordGame(app)
        self._wait_for_started_event = asyncio.Event()

    async def wait_until_started(self) -> bool:
        """Wait until the game starts. Return `False` if the game timed out."""
        return await utils.event_or_timout(self.start_game_timeout, self._wait_for_started_event)

    async def loop(self) -> None:
        """The main game loop"""

        while True:
            await self._round()

    async def _round(self) -> None:
        from bot.game.round import build_card_buttons

        for player in self.players:
            player.clear()

        await self._send_stats()

        await self.discord.respond_to_player(
            0,
            content="Select your cards:",
            component=await build_card_buttons(self.players[0], self),
        )
        await self.discord.respond_to_player(
            1,
            content="Select your cards:",
            component=await build_card_buttons(self.players[1], self),
        )

        start = time.time()

        await utils.event_or_timout(20, *(player.selected_card_event for player in self.players))

        await asyncio.sleep(max(8, time.time() - start))

        await self.discord.delete_responses()

        await self._send_result()

    async def _send_stats(self) -> None:
        await self.discord.respond_global(content="These are some stats.")

    async def _send_result(self) -> None:
        await self.discord.respond_global(
            content=f"{self.players[0].user.mention} selected: {self.players[0].selected_card}"
            f"\n{self.players[1].user.mention} selected: {self.players[1].selected_card}"
        )
