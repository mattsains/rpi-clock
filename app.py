from PIL import ImageTk, Image
from tkinter import Tk, Canvas
import sys
from do_later import Fork

import ui

is_linux = sys.platform == "linux"

if (is_linux):
    pass # todo Raspberry code.
else:
    # hacky tkinter code for testing on a desktop environment
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
    Fork(ui.start)

    root.bind("<KeyPress>", lambda k: ui.receive_key(0 if k.keysym == "z" else 1))
    root.mainloop()