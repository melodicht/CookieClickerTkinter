import tkinter as tk
import unittest

from App import App
from AutoClickers import AutoClickers
from PurchaseButton import PurchaseButton


class TestPurchaseButton(unittest.TestCase):
    def setUp(self):
        root = tk.Tk()
        self.app = App(master=root)
        auto_clicker_1 = AutoClickers('Factory', 5.0, 15.0, 0)
        auto_clicker_2 = AutoClickers('Farm', 15.0, 45.0, 3)
        self.purchase_button_1 = PurchaseButton(self.app, auto_clicker_1)
        self.purchase_button_2 = PurchaseButton(self.app, auto_clicker_2)

    def tearDown(self):
        if self.app.master:
            self.app.shut_down()

    def test_create_name(self):
        self.assertEqual(
            self.purchase_button_1.cget('text'),
            'Factory | $15.0 | 5.0 cps'
        )
        self.assertEqual(
            self.purchase_button_2.cget('text'),
            'Farm | $45.0 | 15.0 cps'
        )
