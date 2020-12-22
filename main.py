import time
from tkinter import *
from tkinter.messagebox import askyesno
from typing import List
from typing import Tuple

try:
    # Allows the user to run the file even on the absence of pyglet.
    import pyglet
    pyglet.font.add_file("font/langar.ttf")

except ImportError:
    pass
from PIL import Image, ImageTk

from logic import get_file_names_of_pics
from logic import get_my_name


FOLDER = "./assets"  # Path to the folder
DEFAULT_IMAGE = "crown.png"  # The name of the image in the given folder


class Memorize(Tk):
    def __init__(self) -> None:
        super(Memorize, self).__init__()

        self.row_col = (5, 4)

        self.title("Memorize")
        self.geometry("446x610+500+0")
        self.buttons: Button = []
        self.resizable(False, False)
        self.iconbitmap(f"{FOLDER}/crown.ico")

        # same as the file names for the images
        self.button_titles = get_file_names_of_pics(FOLDER,
                                                    avoid=[DEFAULT_IMAGE], extn="png") * 2
        # print(self.button_titles)

        self.pressed_buttons: List[Tuple[int, int]] = []
        self.answers: List[Tuple[int, int]] = []
        self.latest_button: Tuple[str, Button, Tuple[int, int]] = None

        self.tries = 0
        self.score = 0
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

        # The tries label
        self.tries_label = Label(self.title_frame, text=f"Tries: {self.tries}",
                                 font=("langar", 14),  bg="#73b504", padx=(30,))
        self.tries_label.grid(row=0, column=1)

        # The total score label
        self.score_label = Label(self.title_frame, text=f"Score: {self.score}",
                                 font=("langar", 14), padx=(80,), bg="#73b504")
        self.score_label.grid(row=0, column=2)

        self.generate_button()

    def generate_button(self):
        # generate all the 20 buttons
        for _ in range(20):
            btn = Button(self.board_frame, text="title")
            self.buttons.append(btn)

        self.arrange_buttons()

    def arrange_buttons(self):
        # arrange all the buttons
        row_count = 0
        col_count = 0
        for btn in self.buttons:
            btn.grid(row=row_count, column=col_count, padx=3, pady=3)
            text = get_my_name(self.button_titles)
            btn.config(command=lambda text=text, row_count=row_count, col_count=col_count, obj=btn, : self.button_pressed(
                obj, text, row_count, col_count),
                text=text)

            col_count += 1
            if col_count == self.row_col[1]:
                col_count = 0
                row_count += 1

        self.set_default_image()

    def set_default_image(self):
        # add the default image
        img = Image.open(f"{FOLDER}/{DEFAULT_IMAGE}")
        img = img.resize((100, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(img)
        for btn in self.buttons:
            btn.config(image=image)
            btn.image = image

    # verify the selection
    def button_pressed(self, obj: Button, title: str, row: int,
                       col: int) -> None:

        # print(title)

        # check whether the button pressed is not the button that is already pressed and the button
        # has not bee selected as a pair(the two identical buttons have been found)
        if (row, col) not in self.pressed_buttons and (row, col) not in self.answers:
            self.add_new_button_info((row, col))

            image = Image.open(f"{FOLDER}/{title}")
            image = image.resize((100, 100), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)
            obj.config(image=image)
            obj.image = image

            if not self.first_button_pressed:
                self.first_button_pressed = True
                self.latest_button = (title, obj, (row, col))

            elif self.first_button_pressed:
                self.tries += 1
                self.first_button_pressed = False
                if title == self.latest_button[0]:
                    self.answers.append((row, col))
                    self.answers.append(self.latest_button[2])

                    # If we get the pair. then disable the button so that its no longer clickable
                    obj["state"] = DISABLED
                    self.latest_button[1]["state"] = DISABLED

                    self.score += 1  # we got a perfect match

                else:

                    def change():
                        self.change_to_default_image(obj)
                        self.change_to_default_image(self.latest_button[1])
                        self.pressed_buttons.clear()

                    self.after(250, change)

                self.update_tries_and_score()

    def add_new_button_info(self, row_col: Tuple[int, int]):
        if not row_col in self.pressed_buttons:
            self.pressed_buttons.append(row_col)

    def change_to_default_image(self, obj: Button) -> None:
        # time.sleep(0.5)
        d_img = Image.open(f"{FOLDER}/{DEFAULT_IMAGE}")
        d_img = d_img.resize((100, 100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(d_img)

        obj.config(image=img)
        obj.image = img

    def update_tries_and_score(self):
        self.tries_label.config(text=f"Tries: {self.tries}")
        self.score_label.config(text=f"Score: {self.score}")

        if self.score == 10:
            self.after(10, self.win_message)

    def win_message(self):
        message = f"Yay !! You won, it took you {self.tries} tries ..\n Would you like to continue ?"

        yes = askyesno("You Won", message=message)
        if yes:
            self.restart()

        else:
            self.quit()
            self.destroy()

    def restart(self):
        self.quit()
        self.destroy()

        Memorize().mainloop()


if __name__ == "__main__":
    memo = Memorize()
    memo.mainloop()
