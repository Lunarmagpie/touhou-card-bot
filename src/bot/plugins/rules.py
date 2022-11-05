import utils
import crescent
from cards.card import Elements, icons

plugin = utils.Plugin()

@plugin.include
@crescent.command(description="View the rules of the game.")
async def rules(ctx: utils.Context) -> None:
    await ctx.respond(f"""
Each card belongs to one of 5 different phases: {icons[Elements.FIRE]} Fire, {icons[Elements.WATER]} Water, {icons[Elements.WOOD]} Wood, {icons[Elements.METAL]} Metal, and {icons[Elements.EARTH]} Earth

In addition, each phase obeys 2 different sets of interactions:
**Weakening Cycle**
{icons[Elements.WOOD]} Wood > {icons[Elements.WATER]} Water > {icons[Elements.METAL]} Metal > {icons[Elements.EARTH]} Earth > {icons[Elements.FIRE]} Fire > {icons[Elements.WOOD]} Wood
**Overcoming Cycle**
{icons[Elements.WOOD]} Wood > {icons[Elements.EARTH]} Earth > {icons[Elements.WATER]} Water > {icons[Elements.FIRE]} Fire > {icons[Elements.METAL]} Metal > {icons[Elements.WOOD]} Wood

Or, arranged differently:
{icons[Elements.FIRE]}{icons[Elements.METAL]}` > `{icons[Elements.WOOD]}` > `{icons[Elements.EARTH]}{icons[Elements.WATER]}
{icons[Elements.METAL]}{icons[Elements.WOOD]}` > `{icons[Elements.EARTH]}` > `{icons[Elements.WATER]}{icons[Elements.FIRE]}
{icons[Elements.WOOD]}{icons[Elements.EARTH]}` > `{icons[Elements.WATER]}` > `{icons[Elements.FIRE]}{icons[Elements.METAL]}
{icons[Elements.EARTH]}{icons[Elements.WATER]}` > `{icons[Elements.FIRE]}` > `{icons[Elements.METAL]}{icons[Elements.WOOD]}
{icons[Elements.WATER]}{icons[Elements.FIRE]}` > `{icons[Elements.METAL]}` > `{icons[Elements.WOOD]}{icons[Elements.EARTH]}

To win a round, a card's phase must conquer the other. If two cards are of the same phase, the card with the higher number wins. After a round is won, a seal of the card's phase is obtained.

To win a game, one must collect 1 seal of 4 different phases, or 3 seals of the same phase.
""", ephemeral=True)
