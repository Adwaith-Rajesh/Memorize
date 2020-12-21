from tkinter import *
from typing import List
from typing import Tuple

import pyglet
from PIL import Image, ImageTk

from logic import get_file_names_of_pics
from logic import get_my_name

pyglet.font.add_file("font/langar.ttf")


class Memorize(Tk):
    def __init__(self) -> None:
        super(Memorize, self).__init__()

        self.row_col = (5, 4)

        self.title("Memorize")
        self.geometry("446x610+500+0")
        self.buttons: Button = []
        self.resizable(False, False)

        # same as the file names for the images
        self.button_titles = get_file_names_of_pics("./assets",
                                                    avoid=["crown.png"]) * 2

        self.pressed_buttons: List[Tuple[int, int]] = []
        self.latest_button: str = ""

        self.first_button_pressed: bool = False
        self.setup_ui()

    def setup_ui(self):

        # TODO: set a specific width and height to all the entities

        # The title frame
        self.title_frame = Frame(self, height=60, bg="#73b504")
        self.title_frame.pack(side=TOP, anchor=NW, fill=X)
        self.title_frame.pack_propagate(False)

        # The main frame
        self.board_frame = Frame(self, bg="#80c904", height=300)
        self.board_frame.pack_propagate(False)
        self.board_frame.pack(side=TOP, anchor=NW, fill=BOTH, pady=(10, 0))

        # Add the title label
        self.title_label = Label(self.title_frame,
                                 text="Memorize",
                                 font=("langar", 16),
                                 bg="#73b504")
        self.title_label.grid(row=0, column=0)

        # generate all the 20 buttons
        for _ in range(20):
            btn = Button(self.board_frame, text="title")
            self.buttons.append(btn)

        # arrange all the buttons
        row_count = 0
        col_count = 0
        for btn in self.buttons:
            btn.grid(row=row_count, column=col_count, padx=3, pady=3)
            text = get_my_name(self.button_titles)
            btn.config(command=lambda text=text, row_count=row_count, col_count
                       =col_count, obj=btn, : self.button_pressed(
                           obj, text, row_count, col_count),
                       text=text)

            col_count += 1
            if col_count == self.row_col[1]:
                col_count = 0
                row_count += 1

        # add the default image image
        img = Image.open("assets/crown.png")
        img = img.resize((100, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        for btn in self.buttons:
            btn.config(image=image)
            btn.image = image

        # verify the selection
    def button_pressed(self, obj: Button, title: str, row: int,
                       col: int) -> None:

        if (row, col) not in self.pressed_buttons:
            print(row, col)
            self.add_new_button_info((row, col))

            image = Image.open(f"./assets/{title}")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            obj.config(image=image)
            obj.image = image

            if not self.first_button_pressed:
                print("False If")
                self.first_button_pressed = True
                self.latest_button = title

            elif self.first_button_pressed:
                self.first_button_pressed = False
                if title == self.latest_button:
                    print("got it")

    def add_new_button_info(self, row_col: Tuple[int, int]):
        if not row_col in self.pressed_buttons:
            self.pressed_buttons.append(row_col)

    def change_to_default_image(self, obj: Button) -> None:
        d_img = Image.open("./assets/crown.png")
        d_img = d_img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(d_img)

        obj.config(image=img)
        ogj.image = img


if __name__ == "__main__":
    memo = Memorize()
    memo.mainloop()