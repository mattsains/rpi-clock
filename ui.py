from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep

display_size = (212, 104)
WHITE = 0
BLACK = 1
YELLOW = 2

class Ui:
    def __init__(self, ask_redraw):
        self.ask_redraw = ask_redraw
    
    """Blocking function to handle the UI"""
    def start(self):
        self.state = {}
        while True:
            self.update()
            self.draw()
            sleep(1)
    
    def update(self):
        pass
    
    def draw(self):
        img = Image.new("P", display_size)
        img.putpalette([
            242, 240, 227, 255,
            43, 38, 32, 255,
            214, 176, 3, 255
        ], 'RGBA')
        img_drawer = ImageDraw.Draw(img)

        current_time = datetime.now().strftime("%H:%M %p")

        img_drawer.text((106, 20), current_time, YELLOW, font=ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 40), anchor='mm')
        img_drawer.text((105, 21), current_time, BLACK, font=ImageFont.truetype('C:\Windows\Fonts\\ariblk.ttf', 40), anchor='mm')

        img_drawer.rectangle((5, 50, 55, 100), BLACK)

        if ('key' in self.state): img_drawer.line([(50, 50), (150, 50), (150, 150), (50, 150), (50, 50)])

        self.ask_redraw(img)

    def receive_key(self, k):
        self.state['key'] = k