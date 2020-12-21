from tkinter import *

import pyglet
from PIL import Image, ImageTk

pyglet.font.add_file("font/langar.ttf")


class Memorize(Tk):
    def __init__(self) -> None:
        super(Memorize, self).__init__()

        self.row_col = (5, 4)

        self.title("Memorize")
        self.geometry("468x645+500+0")
        self.buttons: Button = []
        # self.resizable(False, False)

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
            btn = Button(self.board_frame, text="test")
            self.buttons.append(btn)

        # arrange all the buttons
        row_count = 0
        col_count = 0
        for btn in self.buttons:
            btn.grid(row=row_count, column=col_count, padx=3, pady=3)

            col_count += 1
            if col_count == self.row_col[1]:
                col_count = 0
                row_count += 1

        # add the image
        img = Image.open("assets/crown.png")
        img = img.resize((100, 100), Image.ANTIALIAS)
        # image = PhotoImage(file="assets/crown.png")
        image = ImageTk.PhotoImage(img)
        for btn in self.buttons:
            btn.config(image=image)
            btn.image = image

        # verify the selection
        def button_pressed(self, obj: Button, row: int, col: int) -> None:
            if not self.first_button_pressed:
                self.first_button_pressed = False


if __name__ == "__main__":
    memo = Memorize()
    memo.mainloop()