import crescent
import flare

import cards
import hikari
import utils
import typing as t
import asyncio

CARD_AMOUNT = len(cards.CARDS)
PAGES = CARD_AMOUNT // 16 + 1

plugin = utils.Plugin()
P = t.ParamSpec("P")
T = t.TypeVar("T")
group = crescent.Group("deck")


@t.runtime_checkable
class HasPage(t.Protocol):
    page: int


class CardButton(flare.Button, label=" ", style=hikari.ButtonStyle.SECONDARY):
    x: int
    y: int
    page: int

    async def callback(self, ctx: flare.Context) -> None:
        await ctx.respond(f"{self.x} {self.y} {self.page}", flags=hikari.MessageFlag.EPHEMERAL)


class NextButton(flare.Button, label="Next"):
    page: int

    async def callback(self, ctx: flare.Context) -> None:
        rows = await ctx.get_components()
        new_page = self.page + 1

        if new_page >= PAGES:
            new_page = 0

        for row in rows:
            for component in row:
                if isinstance(component, HasPage):
                    component.page = new_page

        await ctx.edit_response(components=await asyncio.gather(*rows))


class PrevButton(flare.Button, label="Previous"):
    page: int

    async def callback(self, ctx: flare.Context) -> None:
        rows = await ctx.get_components()
        new_page = self.page - 1

        if new_page < 0:
            new_page = PAGES - 1

        for row in rows:
            for component in row:
                if isinstance(component, HasPage):
                    component.page = new_page

        await ctx.edit_response(components=await asyncio.gather(*rows))


@flare.button(label="Show Deck")
async def show_button(ctx: flare.Context, user_id: hikari.Snowflake) -> None:
    await ctx.edit_response("YOUR DECK", flags=hikari.MessageFlag.EPHEMERAL)


@flare.button(label="Close")
async def close_button(ctx: flare.Context) -> None:
    ...


@plugin.include
@group.child
@crescent.command(description="Edit your card decks.")
class edit:
    name = crescent.option(str, "The name of the deck you want to edit")

    async def callback(self, ctx: utils.Context) -> None:
        await ctx.respond(
            # fmt: off
            components=await asyncio.gather(
                flare.Row(CardButton(0, 0, 0), CardButton(1, 0, 0), CardButton(2, 0, 0), CardButton(3, 0, 0), CardButton(4, 0, 0)),
                flare.Row(CardButton(0, 1, 0), CardButton(1, 1, 0), CardButton(2, 1, 0), CardButton(3, 1, 0), CardButton(4, 1, 0)),
                flare.Row(CardButton(0, 2, 0), CardButton(1, 2, 0), CardButton(2, 2, 0), CardButton(3, 2, 0), CardButton(4, 2, 0)),
                flare.Row(CardButton(0, 3, 0), CardButton(1, 3, 0), CardButton(2, 3, 0), CardButton(3, 3, 0), CardButton(4, 3, 0)),
                flare.Row(NextButton(0), PrevButton(0), show_button(ctx.user.id)),
            ),
            # fmt: on
            ephemeral=True
        )
