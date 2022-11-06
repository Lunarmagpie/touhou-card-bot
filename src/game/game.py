import asyncio
import random
import time
import typing as t

import flare
import hikari

import cards
import utils
import visuals
from game.discord_game import DiscordGame
from game.player import Player


class Game:
    def __init__(self, app: utils.Bot, players: tuple[hikari.User, hikari.User]) -> None:
        self.players = (Player(players[0]), Player(players[1]))
        self.discord = DiscordGame(app)
        self._countdown: str | None = None
        self.previous_round_results: tuple[Player, Player] | None = None

    @property
    def countdown(self) -> str:
        assert self._countdown
        return self._countdown

    @countdown.setter
    def countdown(self, value: str) -> None:
        self._countdown = value

    async def loop(self) -> None:
        """The main game loop"""

        await self._send_stats()

        while True:
            await self._round()

    async def _round(self) -> None:
        from game import components

        for player in self.players:
            player.on_round_start()

        async with utils.TaskGroup() as tg:
            player_1 = self.players[0]
            player_1_hand = tg.create_task(visuals.get_hand_image(player_1.hand))
            player_1_buttons = tg.create_task(
                components.build_card_buttons(player_1, self, len(player_1.hand))
            )

            player_2 = self.players[1]
            player_2_hand = tg.create_task(visuals.get_hand_image(player_2.hand))
            player_2_buttons = tg.create_task(
                components.build_card_buttons(player_2, self, len(player_2.hand))
            )

        content = (
            "Select a blurple button to pick a card. Select a gray button to check"
            " the card's information."
        )

        async with utils.TaskGroup() as tg:
            tg.create_task(
                self.discord.respond_to_player(
                    0,
                    content=content,
                    attachment=player_1_hand.result(),
                    components=player_1_buttons.result(),
                )
            )
            tg.create_task(
                self.discord.respond_to_player(
                    1,
                    content=content,
                    attachment=player_2_hand.result(),
                    components=player_2_buttons.result(),
                )
            )

        start = time.time()

        await utils.event_or_timout(20, *(player.selected_card_event for player in self.players))

        time_waited = time.time() - start

        if time_waited < 8:
            await asyncio.sleep(8 - time_waited)

        await self.discord.delete_ephermial_responses()
        await self.discord.delete_global_response()

        if round_res := self.get_results():
            self.previous_round_results = round_res
            winner, loser = round_res
            await self._send_stats(
                content=f"Winner: {winner.user.mention}\nLoser: {loser.user.mention}",
            )
        else:
            self.previous_round_results = None
            await self._send_stats(content="There was a tie")

        await asyncio.sleep(8)

    def get_results(self) -> tuple[Player, Player] | None:
        # If a player didn't pick a card, choose a card for them.
        for player in self.players:
            if not player.selected_card:
                player.selected_card = player.hand.pop(random.choice(range(len(player.hand))))

        assert self.players[0].selected_card
        assert self.players[1].selected_card

        res = cards.get_interaction_result(
            self.players[0].selected_card, self.players[1].selected_card
        )

        match res:
            case cards.InteractionResults.P1_WIN:
                self.players[0].add_seal()
                return (self.players[0], self.players[1])
            case cards.InteractionResults.P2_WIN:
                self.players[1].add_seal()
                return (self.players[1], self.players[0])
            case cards.InteractionResults.TIE:
                return None

    async def _send_stats(self, **kwargs: t.Any) -> None:
        from game import components

        self.countdown = utils.countdown(20)

        player_names = visuals.format_names(
            self.players[0].user.username, self.players[1].user.username, length=40
        )
        player_seals = visuals.format_seals(self.players[0].seals, self.players[1].seals, length=17)

        embed = hikari.Embed(
            title="Game 1",
            description=visuals.format_results(
                self.players[0], self.players[1], self.previous_round_results
            ),
        )
        embed.add_field(
            player_names,
            player_seals,
            inline=False,
        )
        embed.add_field(str(visuals.Emoji.BLANK), f"Next round {self.countdown}")

        await self.discord.respond_global(
            embed=embed,
            component=await flare.Row(
                components.show_card_selection(self.players[0], self.players[1], self)
            ),
            **kwargs,
        )
