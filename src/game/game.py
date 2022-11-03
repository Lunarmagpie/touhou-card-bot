import hikari
import asyncio

from game.discord_game import DiscordGame
from game.player import Player
import images
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
            player.on_round_start()

        self.countdown = utils.countdown(20)

        await self._send_stats()

        for i in range(2):
            player = self.players[i]

            asyncio.ensure_future(
                self.discord.respond_to_player(
                    i,
                    content=(
                        "Select a blurple buttton to pick a card. Select a gray button to check"
                        " the card's information."
                    ),
                    attachment=await images.get_hand_image(player.hand),
                    components=await components.build_card_buttons(player, self, len(player.hand)),
                )
            )

        start = time.time()

        await utils.event_or_timout(20, *(player.selected_card_event for player in self.players))

        time_waited = time.time() - start

        if time_waited < 8:
            await asyncio.sleep(8 - time_waited)

        await self.discord.delete_responses()

    async def _send_stats(self) -> None:
        from game import components

        embed = hikari.Embed(title="Game 1", description=f"Next round {self.countdown}.")
        embed.add_field(self.players[0].user.username, "score", inline=True)
        embed.add_field(self.players[1].user.username, "score", inline=True)

        await self.discord.respond_global(
            content=embed,
            component=await flare.Row(
                components.show_card_selection(self.players[0], self.players[1], self)
            ),
        )
