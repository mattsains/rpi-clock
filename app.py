from PIL import Image
import sys
from src import do_later
from src import ui

is_linux = sys.platform == "linux"

if (is_linux):
    from inky import auto
    inky_display = auto()

    def update(i: Image):
        inky_display.set_image(i)
        inky_display.show()
    
    ui = ui.Ui(update)
    do_later.Fork(ui.start)
else:
    # hacky tkinter code for testing on a desktop environment
    from tkinter import Tk, Canvas
    from PIL import ImageTk
    last_image = [None]
    root = Tk()
    root.title("Clock preview")
    root.geometry("430x214")
    cv = Canvas()
    cv.pack(side='top', fill='both', expand='yes')

    def update(i: Image):
        try:
            i = i.resize((424, 208), Image.BOX)
            last_image[0] = ImageTk.PhotoImage(i)
            cv.create_rectangle(2, 2, 427, 211, outline="black", fill="white")
            cv.create_image(3, 3, image=last_image[0], anchor='nw')
        except:
            exit(0)
    
    ui = ui.Ui(update)
    do_later.Fork(ui.start)

    root.bind("<KeyPress>", lambda k: ui.receive_key(0 if k.keysym == "z" else 1))
    root.mainloop()