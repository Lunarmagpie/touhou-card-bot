from faulthandler import disable
import crescent
import flare

import cards
import hikari
import utils
import typing as t
import asyncio
import visuals

CARD_AMOUNT = len(cards.CARDS)
PAGES = CARD_AMOUNT // 16 + 1

plugin = utils.Plugin()
P = t.ParamSpec("P")
T = t.TypeVar("T")
group = crescent.Group("deck")

#EXAMPLE VARIABLE TO MAKE SURE EVERYTHING WORKS DELETE THIS LATER
cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,25,29,30]


@t.runtime_checkable
class HasPage(t.Protocol):
    page: int


class CardButton(flare.Button, label=" ", style=hikari.ButtonStyle.SECONDARY):
    x: int
    y: int
    page: int

    async def try_disable(self, ctx: flare.Context):
        if self.x * 5 + self.y + self.page * 20 + 2 not in cards:
            self.set_disabled(True)
        else:
            self.set_disabled(False)

    async def callback(self, ctx: flare.Context) -> None:
        await ctx.respond(f"{self.x} {self.y} {self.page}", flags=hikari.MessageFlag.EPHEMERAL)


class NextButton(flare.Button, label="Next"):
    page: int

    async def try_disable(self, ctx: flare.Context):
        ...

    async def callback(self, ctx: flare.Context) -> None:
        rows = await ctx.get_components()
        new_page = self.page + 1

        if new_page >= PAGES:
            new_page = 0

        for row in rows:
            for component in row:
                if isinstance(component, HasPage):
                    component.page = new_page
                    await component.try_disable(ctx)

        await ctx.edit_response(components=await asyncio.gather(*rows))


class PrevButton(flare.Button, label="Previous"):
    page: int

    async def try_disable(self, ctx: flare.Context):
        ...

    async def callback(self, ctx: flare.Context) -> None:
        rows = await ctx.get_components()
        new_page = self.page - 1

        if new_page < 0:
            new_page = PAGES - 1

        for row in rows:
            for component in row:
                if isinstance(component, HasPage):
                    component.page = new_page
                    await component.try_disable(ctx)

        await ctx.edit_response(components=await asyncio.gather(*rows))


@flare.button(label="Show Deck")
async def show_button(ctx: flare.Context, user_id: hikari.Snowflake) -> None:
    await ctx.edit_response("YOUR DECK", flags=hikari.MessageFlag.EPHEMERAL)


@flare.button(label="Close")
async def close_button(ctx: flare.Context) -> None:
    ...

async def build_rows(ctx, cards: list[int], page: int) -> list[flare.Row]:
    rows = []

    for i in range(0,4):
        rows.append(flare.Row())
        for j in range(0,5):
            if i * 5 + j + page * 20 + 2 in cards:
                rows[i].append(CardButton(i, j, page))
            else:
                rows[i].append(CardButton(i, j, page).set_disabled(True))

    rows.append(flare.Row(NextButton(page), PrevButton(page), show_button(ctx.user.id)))

    return await asyncio.gather(*rows)


@plugin.include
@group.child
@crescent.command(description="Edit your card decks.")
class edit:
    name = crescent.option(str, "The name of the deck you want to edit")

    async def callback(self, ctx: utils.Context) -> None:
        page = 0
        attachment = await visuals.get_cards_array_image(cards, page)
        await ctx.respond(
            # fmt: off
            components=await build_rows(ctx, cards, page),
            # fmt: on
            ephemeral=True,
            attachment=attachment
        )
