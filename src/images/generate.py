from types import NoneType
from PIL import Image
from cards.card import Card, CARDS 
import time
import os

def generate(cards: list[int]) -> str:
    output_img = Image.new("RGBA", (1340, 360), (255,255,255,0))

    for i,id in enumerate(cards):
        card_img = Image.open(f"./resources/card_png/{CARDS[id].img_name}.png")
        output_img.paste(card_img,(260*i,360 - card_img.height), card_img)

    output_name = str(time.time())
    output_img.save(f"./src/images/{output_name}.png", "PNG")
    return output_name

def remove_image(image_name: list[str]):
    for i in image_name:
        os.remove(f"./src/images/{i}.png")