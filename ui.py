from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from do_later import DoLater, RepeatLater

display_size = (212, 104)
WHITE = 0
BLACK = 1
YELLOW = 2

class Ui:
    def __init__(self, ask_redraw):
        self.ask_redraw = ask_redraw
        
        self.draw()
        RepeatLater(self.draw, 60)
    
    def draw(self):
        self.img = Image.new("P", display_size)
        self.img.putpalette([
            242, 240, 227, 255,
            43, 38, 32, 255,
            214, 176, 3, 255
        ], 'RGBA')
        self.draw = ImageDraw.Draw(self.img)

        now = datetime.now()
        current_time = now.strftime("%H:%M")

        self.draw.text((106, 52), current_time, YELLOW, font=ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 40), anchor='mm')

        self.ask_redraw(self.img)


    def receive_key(self, k):
        self.draw.line([(50, 50), (150, 50), (150, 150), (50, 150), (50, 50)])
        self.ask_redraw(self.img)