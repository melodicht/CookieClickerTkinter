import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from GameManager import GameManager
from PurchaseButton import PurchaseButton


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Cookie Clicker")
        self.master.geometry("400x400")
        self.master.protocol("WM_DELETE_WINDOW", self.shut_down)

        self.cookie_number_display = tk.StringVar()
        self.message_display = tk.StringVar()

        self.init_game_manager()

        self.pack()
        self.create_widgets()

    def init_game_manager(self):
        self.game_manager = GameManager(self)

    def configure_styles(self):
        style = ThemedStyle(self.master)
        style.set_theme("default")

        style.configure(
            'TButton',
            foreground="black",
            background="white",
            borderwidth=0,
            highlightthickness=0,
            font=('MS Reference Sans Serif', 15)
        )

    def create_widgets(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame['bg'] = "white"
        self.button_frame['highlightthickness'] = "0"
        self.button_frame.place(relx=0, rely=0, relwidth=57, relheight=1)

        self.create_click_cookie_button()
        self.create_purchase_buttons()
        self.create_cookie_number_display()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.shut_down)
        self.quit.pack(side="bottom")

    def create_click_cookie_button(self):
        self.click_button = ttk.Button(
            self.button_frame,
            style="TButton",
            text="Click for Cookies!",
            width=57,
            command=self.game_manager.player_click
        )
        self.click_button.pack(side=tk.LEFT)
        self.click_button.config(width=3)

    def create_purchase_buttons(self):
        auto_clickers_dict = self.game_manager.auto_clickers

        i = 1
        for ac in auto_clickers_dict.values():
            new_button = PurchaseButton(self, ac)
            # new_button.grid(row=i, column=1)
            i += 1

    def create_cookie_number_display(self):
        self.cookie_label = tk.Label(
            self.master, textvariable=self.cookie_number_display, width=57
        )
        self.cookie_label.pack()

    def update_cookie_number_display(self, num):
        num = round(num, 1)  # Round to one decimal place
        self.cookie_number_display.set(
            "You have " + str(num) + " cookies!"
        )

    def alert_user(self, text):
        message_sv = tk.StringVar()
        message_sv.set(text)

        message = tk.Label(self.master, textvariable=message_sv)
        message.pack()

        def on_after():
            message_sv.set('')  # Make it empty so it disappears
            message.forget()

        message.after(1500, on_after)

    def shut_down(self):
        self.game_manager.cps_event.clear()
        self.game_manager.cps_thread.join()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
