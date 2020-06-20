import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from GameManager import GameManager
from PurchaseButton import PurchaseButton


class App(tk.Frame):
    """
    The application instance that contains the tkinter root.

    Attributes
    ----------
    master : tk.Tk()
    cookie_number_display : tk.StringVar()
    cps_display : tk.StringVar()
    message_display : tk.StringVar()
    game_manager : GameManager

    Methods
    -------
    update_cookie_number_display(num)
        Updates `cookie_number_display` to its appropriate value.
    update_cps_display(num)
        Updates `cps_display` to its appropriate value.
    alert_user(text)
        Creates a text label, with `text` to inform the user.
    shut_down()
        Destroys the application root and closes the threads.

    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Cookie Clicker")
        self.master.geometry("400x400")
        self.master.protocol("WM_DELETE_WINDOW", self.shut_down)

        self.cookie_number_display = tk.StringVar()
        self.cps_display = tk.StringVar()
        self.message_display = tk.StringVar()

        self.init_game_manager()

        self.pack()
        self.create_widgets()

    def init_game_manager(self):
        """Initialise the game manager instance."""
        self.game_manager = GameManager(self)

    def configure_styles(self):
        """Create the ttk.style styles."""
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
        """Create the appropriate display for the application."""
        # Create the button frame
        self.button_frame = tk.Frame(self.master)
        self.button_frame['bg'] = "white"
        self.button_frame['highlightthickness'] = "0"
        self.button_frame.place(relx=0, rely=0, relwidth=57, relheight=1)

        # Create the appropriate buttons for the application
        self.create_click_cookie_button()
        self.create_purchase_buttons()
        self.create_cookie_number_display()
        self.create_cps_display()

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

    def create_cps_display(self):
        self.cps_label = tk.Label(
            self.master, textvariable=self.cps_display, width=57
        )
        self.cps_label.pack()

    def update_cookie_number_display(self, num):
        num = round(num, 1)  # Round to one decimal place
        self.cookie_number_display.set(
            "You have " + str(num) + " cookies!"
        )

    def update_cps_display(self, num):
        num = round(num, 1) # Round to one decimal place
        self.cps_display.set(
            "Automatic Clicks per Second: " + str(num)
        )

    def alert_user(self, text):
        """Creates a temporary text label and deletes it after 1.5s."""
        message_sv = tk.StringVar()
        message_sv.set(text)

        message = tk.Label(self.master, textvariable=message_sv)
        message.pack()

        def on_after():
            message_sv.set('')  # Make it empty so it disappears
            message.forget()

        message.after(1500, on_after)

    def shut_down(self):
        """Close the threads and destroy the application root."""
        self.game_manager.cps_event.clear()
        self.game_manager.cps_thread.join()
        self.master.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
