import tkinter as tk
from tkinter import ttk


class PurchaseButton(ttk.Button):
    def __init__(self, app, auto_clicker_type):
        self.ac_type = auto_clicker_type
        super().__init__(
            app.button_frame,
            style="TButton",
            text=self.create_name(),
            width=57,
            command=lambda: app.game_manager.buy_auto_clicker(
                self.ac_type.name
            )
        )
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(self.create_name()))

    def create_name(self):
        text = ' | '.join([
            self.ac_type.name,
            '$' + str(self.ac_type.unit_price),
            str(self.ac_type.cookies_per_second) + ' cps'
        ])
        return text
