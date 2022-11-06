import crescent
import hikari

import utils

plugin = utils.Plugin()
group = crescent.Group("deck")

@flare.button()
async def card_button(ctx: flare.Context, page: int, x: int, y: int) -> None:


@plugin.include
@group.child
@crescent.command(description="Edit your card decks.")
class edit:
    name = crescent.option(str, "The name of the deck you want to edit")

    async def callback(self, ctx: utils.Context) -> None:
        player_info = ctx.app.db.fetch_player(ctx.user.id)



        await ctx.respond(
            ,
            ephemeral=True,
        )
