import utils
import crescent

plugin = utils.Plugin()


@plugin.include
@crescent.command(description="Pong!")
async def ping(ctx: utils.Context) -> None:
    await ctx.respond(f"Pong! ({round(ctx.app.heartbeat_latency * 1_000 * 100)/100}ms)")
