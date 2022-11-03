from PIL import Image
from cards.card import CARDS
import hikari
import asyncio
import io
import typing as t
import functools

__all__: t.Sequence[str] = ("get_hand_image",)


async def get_hand_image(cards: list[int]) -> hikari.Bytes:
    output_img = Image.new("RGBA", (1340, 360), (255, 255, 255, 0))

    for i, id in enumerate(cards):
        card_img = Image.open(f"resources/card_png/{CARDS[id].img_name}.png")
        await asyncio.get_event_loop().run_in_executor(
            None,
            functools.partial(card_img.load),
        )
        output_img.paste(card_img, (260 * i, 360 - card_img.height), card_img)

    with io.BytesIO() as b:
        output_img.save(b, format="png")
        return hikari.Bytes(b.getvalue(), "card_display.png")
