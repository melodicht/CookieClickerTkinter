import threading
import time

from AutoClickers import AutoClickers


class GameManager:
    app = None

    def __init__(self, app_instance=None, auto_clickers=None):
        if auto_clickers is None:
            self.create_auto_clickers()
        else:
            self.auto_clickers = self.convert_to_dictionary_format(
                auto_clickers
            )
        self.cookies = 0

        self.app = app_instance

        self.cps_event = threading.Event()

        # Begin cps thread
        self.cps_thread = threading.Thread(
            target=self.add_cookies_every_second
        )
        self.cps_thread.start()
        self.cps_event.set()

    def create_auto_clickers(self):
        ac_1 = AutoClickers('Dough Roller', 0.1, 50, 0)
        ac_2 = AutoClickers('Secret Recipe', 0.5, 100, 0)
        ac_3 = AutoClickers('Small Bussiness', 2.0, 200, 0)

        self.auto_clickers = self.convert_to_dictionary_format(
            [ac_1, ac_2, ac_3]
        )

    def convert_to_dictionary_format(self, auto_clickers):
        the_dict = {au_c.name: au_c for au_c in auto_clickers}
        return the_dict

    def buy_auto_clicker(self, name):
        if self.auto_clickers[name].is_affordable(self.cookies):
            self.auto_clickers[name].buy(self.cookies)
            self.cookies -= self.auto_clickers[name].unit_price
            self.app.update_cookie_number_display(self.cookies)
        else:
            if self.app is not None:
                self.app.alert_user('You do not have enough cookies!')

    def player_click(self):
        self.cookies += 1
        self.app.update_cookie_number_display(self.cookies)

    @property
    def total_auto_clicks_per_second(self):
        return sum(
            au_c.player_quantity * au_c.cookies_per_second
            for au_c in self.auto_clickers.values()
        )

    def add_cookies_every_second(self):
        self.cps_event.wait()
        while self.cps_event.is_set():
            self.cookies += self.total_auto_clicks_per_second
            if self.app is not None:
                self.app.update_cookie_number_display(self.cookies)
            time.sleep(1)  # Wait one second


# Testing purposes:
# auto_clicker_1 = AutoClickers('Factory', 5.0, 15.0, 0)
# auto_clicker_2 = AutoClickers('Farm', 10.0, 50.0, 3)
# auto_clicker_3 = AutoClickers('House', 20.0, 100.0, 5)
# game_manager = GameManager(
#     auto_clickers=[
#         auto_clicker_1, auto_clicker_2, auto_clicker_3
#     ]
# )
