
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Desktop\Documents\Programming\Python\Cutting-Stock-Branch-and-Bound\GUI\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("395x523")
window.configure(bg = "#001524")


canvas = Canvas(
    window,
    bg = "#001524",
    height = 523,
    width = 395,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    197.0,
    301.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    197.0,
    212.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#98C1D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=48.0,
    y=186.0,
    width=298.0,
    height=50.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    197.0,
    296.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#98C1D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=48.0,
    y=270.0,
    width=298.0,
    height=50.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    196.0,
    447.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#98C1D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=47.0,
    y=404.0,
    width=298.0,
    height=84.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=115.0,
    y=336.0,
    width=162.0,
    height=36.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=35.0,
    y=35.0,
    width=77.0,
    height=22.0
)
window.resizable(False, False)
window.mainloop()
