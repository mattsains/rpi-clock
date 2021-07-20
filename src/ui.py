from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
from ttf_opensans import opensans

from dataclasses import dataclass
from typing import Optional, List
from .do_later import RepeatStartingNow

from .weather import WeatherInfo, get_weather
from .ui_helpers import draw_outlined_text, draw_shadow_text

display_size = (250, 122)
WHITE = 0
BLACK = 1
YELLOW = 2

sans = str(opensans(font_weight=1000, italic=False).path)

SANS_50 = ImageFont.truetype(sans, 50)
SANS_20 = ImageFont.truetype(sans, 20)
SANS_10 = ImageFont.truetype(sans, 10)


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
        self.prevState = str(self.state)

        def respondToWeatherUpdate(weather: List[WeatherInfo]):
            self.state.weather = weather
        RepeatStartingNow(lambda: get_weather(respondToWeatherUpdate), 3600)

        while True:
            self.update()
            if (str(self.state) != self.prevState):
                self.draw()
                self.prevState = str(self.state)
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

        time_font_offset = SANS_50.getsize(self.state.timestring)
        draw_shadow_text(img_drawer, (int((display_size[0] - time_font_offset[0])/2), 0), self.state.timestring, BLACK, YELLOW, font=SANS_50)

        if (self.state.weather != None):
            extra_space = display_size[0] - len(self.state.weather) * 50
            position = int(extra_space/2)
            for weather in self.state.weather:
                weather_icon = Image.open(f'icons/{weather.icon}.png')
                self.img.paste(weather_icon, (position, display_size[1]-50))
                time_font_offset = SANS_10.getsize(weather.time)
                img_drawer.text((int(position + 25 - time_font_offset[0]/2), display_size[1]-60), weather.time, BLACK, font=SANS_10)
                temp_font_offset = SANS_20.getsize(weather.temp)
                draw_outlined_text(img_drawer, (int(position + 25 - temp_font_offset[0]/2), display_size[1]-50), weather.temp, BLACK, WHITE, font=SANS_20)
                position += 50

        self.ask_redraw(self.img)

    def receive_key(self, k):
        self.state.key = k