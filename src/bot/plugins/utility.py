import crescent
import hikari

import utils

plugin = utils.Plugin()


@plugin.include
@crescent.command(description="Pong!")
async def ping(ctx: utils.Context) -> None:
    await ctx.respond(f"Pong! ({round(ctx.app.heartbeat_latency * 1_000 * 100)/100}ms)")


@plugin.include
@crescent.command(description="View a card, based on the image name")
async def viewcard(ctx: utils.Context, img_name: str) -> None:
    await ctx.respond(
        "Requested card", attachment=hikari.File(f"resources/card_png/{img_name}.png")
    )
