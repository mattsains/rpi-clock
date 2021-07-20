from sys import argv
from PIL import ImageDraw
from typing import Tuple

def draw_outlined_text(drawer: ImageDraw, xy: Tuple[float, float], text: str, color: int, outline_color: int, *args, **kwargs):
    for x_offset in [-1, 1, 0]:
        for y_offset in [-1, 1, 0]:
            if (x_offset == 0 and y_offset == 0):
                drawer.text((xy[0] + x_offset, xy[1] + y_offset), text, color, *args, **kwargs)
            else:
                drawer.text((xy[0] + x_offset, xy[1] + y_offset), text, outline_color, *args, **kwargs)

def draw_shadow_text(drawer: ImageDraw, xy: Tuple[float, float], text: str, color: int, shadow_color: int, *args, **kwargs):
    drawer.text((xy[0] + 2, xy[1] + 2), text, shadow_color, *args, **kwargs)
    drawer.text((xy[0], xy[1]), text, color, *args, **kwargs)
