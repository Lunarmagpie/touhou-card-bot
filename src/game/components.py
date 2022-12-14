from __future__ import annotations

import asyncio
import contextlib

import flare
import hikari

from cards import CARDS
from game.game import Game
from game.player import Player


@flare.button()
async def card_button(ctx: flare.Context, player: Player, game: Game, number: int) -> None:
    player.selected_card_event.set()
    player.selected_card = player.hand[number]

    # If the interaction is processed after the card selection message is deleted, a
    # forbidden error would be raised.
    with contextlib.suppress(hikari.NotFoundError):
        # Remove the interaction failed response without changing anything.
        await ctx.edit_response()


@flare.button(label="?", style=hikari.ButtonStyle.SECONDARY)
async def info_button(ctx: flare.Context, player: Player, game: Game, number: int) -> None:

    picked_card = CARDS[player.hand[number]]

    await ctx.interaction.create_initial_response(
        hikari.ResponseType.MESSAGE_CREATE,
        f"**{picked_card.name}** ({picked_card.value} of {picked_card.type_icon})"
        f"\n*{picked_card.special_effect_desc}"
        f"\n{picked_card.get_interactions}*",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


async def build_card_buttons(player: Player, game: Game, card_count: int) -> list[flare.Row]:
    rows = [flare.Row(), flare.Row()]

    for i in range(card_count):
        rows[0].append(card_button(player, game, i).set_label(str(i + 1)))
        rows[1].append(info_button(player, game, i))

    return await asyncio.gather(*rows)


@flare.button(label="Reshow Card Selection", style=hikari.ButtonStyle.SECONDARY)
async def show_card_selection(
    ctx: flare.Context, player_one: Player, player_two: Player, game: Game
) -> None:
    if ctx.user.id == player_one.user.id:
        await ctx.respond(
            components=await build_card_buttons(player_two, game, len(player_two.hand)),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    elif ctx.user.id == player_one.user.id:
        await ctx.respond(
            components=await build_card_buttons(player_two, game, len(player_two.hand)),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    else:
        await ctx.respond("You are not part of this game.", flags=hikari.MessageFlag.EPHEMERAL)
