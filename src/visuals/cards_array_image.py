import asyncio
import functools
import io
import typing as t
import math

import hikari
from PIL import Image

import cards

__all__: t.Sequence[str] = ("get_cards_array_image",)


async def get_cards_array_image(player_cards: list[int], page: int) -> hikari.Bytes:
    output_img = Image.new("RGBA", (1350, 1440), (255, 255, 255, 0))

    for i in range(page*20, (page+1)*20):
        x = (i % 5) * 260 - 15
        y = math.floor(i % 20 / 5) * 360

        if (i+2) in player_cards:
            card_img = Image.open(f"resources/card_png/{cards.CARDS[i+2].img_name}.png")
            await asyncio.get_event_loop().run_in_executor(
                None,
                functools.partial(card_img.load),
            )
            output_img.paste(card_img, (x,y + 360 - card_img.height), card_img)
        else:
            card_img = Image.open(f"resources/card_png/blank.png")
            await asyncio.get_event_loop().run_in_executor(
                None,
                functools.partial(card_img.load),
            )
            output_img.paste(card_img, (x,y + 360 - card_img.height), card_img)     

    with io.BytesIO() as b:
        image_resized = output_img.resize((844,900),1)
        image_resized.save(b, format="png")
        b.seek(0)
        return hikari.Bytes(b, "card_display.png")