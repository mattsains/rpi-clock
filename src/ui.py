from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep

from dataclasses import dataclass
from typing import Optional, List
from .do_later import RepeatStartingNow

from .weather import WeatherInfo, get_weather
from .ui_helpers import draw_outlined_text, draw_shadow_text

display_size = (212, 104)
WHITE = 0
BLACK = 1
YELLOW = 2

ARIAL_40 = ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 40)
ARIAL_20 = ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 20)
ARIAL_10 = ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 10)

@dataclass
class InternalDisplayState:
    timestring: Optional[str] = None
    weather: Optional[List[WeatherInfo]] = None
    key: int = None

class Ui:
    def __init__(self, ask_redraw):
        self.ask_redraw = ask_redraw
    
    """Blocking function to handle the UI"""
    def start(self):
        self.state = InternalDisplayState()

        def respondToWeatherUpdate(weather: List[WeatherInfo]):
            self.state.weather = weather
        RepeatStartingNow(lambda: get_weather(respondToWeatherUpdate), 3600)

        while True:
            self.update()
            self.draw()
            sleep(1)

    def update(self):
        self.state.timestring = datetime.now().strftime("%I:%M %p").strip('0')
    
    def draw(self):
        self.img = Image.new("P", display_size)
        self.img.putpalette([
            242, 240, 227,
            43, 38, 32,
            214, 176, 3
        ], 'RGB')
        img_drawer = ImageDraw.Draw(self.img)

        draw_shadow_text(img_drawer, (105, 20), self.state.timestring, BLACK, YELLOW, font=ARIAL_40, anchor='mm')

        if (self.state.weather != None):
            position = 5
            for weather in self.state.weather:
                weather_icon = Image.open(f'icons/{weather.icon}.png')
                self.img.paste(weather_icon, (position, 54))
                img_drawer.text((position + 25, 46), weather.time, BLACK, font=ARIAL_10, anchor='mt')

                draw_outlined_text(img_drawer, (position + 25, 54), weather.temp, BLACK, WHITE, font=ARIAL_20, anchor='mt')
                position += 50

        self.ask_redraw(self.img)

    def receive_key(self, k):
        self.state.key = k