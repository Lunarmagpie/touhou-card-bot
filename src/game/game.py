import hikari
import asyncio

from game.discord_game import DiscordGame
from game.player import Player
import time
import flare
import utils


class Game:
    def __init__(self, app: utils.Bot, players: tuple[hikari.User, hikari.User]) -> None:
        self.players = (Player(players[0]), Player(players[1]))
        self.discord = DiscordGame(app)
        self._countdown: str | None = None

    @property
    def countdown(self) -> str:
        assert self._countdown
        return self._countdown

    @countdown.setter
    def countdown(self, value: str) -> None:
        self._countdown = value

    async def loop(self) -> None:
        """The main game loop"""

        while True:
            await self._round()

    async def _round(self) -> None:
        from game import components

        for player in self.players:
            player.clear()

        self.countdown = utils.countdown(21)
        await self._send_stats()

        await asyncio.gather(
            self.discord.respond_to_player(
                0,
                component=await components.build_card_buttons(self.players[0], self),
            ),
            self.discord.respond_to_player(
                1,
                component=await components.build_card_buttons(self.players[1], self),
            ),
        )

        start = time.time()

        await utils.event_or_timout(20, *(player.selected_card_event for player in self.players))

        time_waited = time.time() - start

        if time_waited < 6:
            await asyncio.sleep(6 - time_waited)

        await self.discord.delete_responses()

        await self._send_result()

    async def _send_stats(self) -> None:
        from game import components

        await self.discord.respond_global(
            content=f"These are some stats.\n{self.countdown}s Remaining",
            component=await flare.Row(
                components.show_card_selection(self.players[0], self.players[1], self)
            ),
        )

    async def _send_result(self) -> None:
        await self.discord.respond_global(
            content=f"{self.players[0].user.mention} selected: {self.players[0].selected_card}"
            f"\n{self.players[1].user.mention} selected: {self.players[1].selected_card}"
        )
