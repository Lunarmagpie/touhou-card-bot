import utils
import flare
import crescent
import hikari
import asyncio

from game import Game

plugin = utils.Plugin()


@flare.button(label="Click to accept.")
async def accept_button(ctx: flare.Context, ev: asyncio.Event, game: Game) -> None:
    if ev.is_set():
        await ctx.respond("This interaction timed out.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    if game.players[1].user.id != ctx.user.id:
        await ctx.respond(
            "Only the mentioned player can accept the challenge.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    game.discord.set_interaction(1, ctx.interaction)
    ev.set()
    await ctx.respond(f"{game.players[1].user.mention} accepted the game.")


@plugin.include
@crescent.command(description="Play a card game vs another player.")
async def play(ctx: utils.Context, opponent: hikari.User) -> None:

    game = Game(
        app=plugin.app,
        players=(ctx.user, opponent),
    )

    game.discord.set_interaction(0, ctx.interaction)

    ev = asyncio.Event()

    await ctx.respond(
        f"{opponent.mention}, accept the challenge!!",
        component=await flare.Row(accept_button(ev, game)),
    )

    if await utils.event_or_timout(30, ev):
        await ctx.respond(
            f"The game could not be started because {opponent.mention} did not accept."
        )
        return

    # Wait a second for visuals.
    await asyncio.sleep(0.5)

    await game.loop()
