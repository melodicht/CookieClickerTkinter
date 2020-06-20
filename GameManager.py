import threading
import time

from AutoClickers import AutoClickers


class GameManager:
    """
    Game manager instance to handle game logistics.

    Attributes
    ----------
    app : tk.Tk()
    auto_clickers : list of AutoClickers
    cps_event : threading.Event()
    cps_thread : threading.Thread()
    cookies : float
    total_auto_clicks_per_second : float

    Methods
    -------
    buy_auto_clicker(name)
    player_click()
    total_auto_clicks_per_second()
    add_cookies_every_second()

    Note
    ----
    The GameManager instance requires the `app_instance` as tk.Tk().

    """
    app = None

    def __init__(self, app_instance=None, auto_clickers=None):
        if auto_clickers is None:
            self.create_auto_clickers()
        else:
            self.auto_clickers = self.convert_to_dictionary_format(
                auto_clickers
            )
        self.app = app_instance

        self.cookies = 0

        if self.app is not None:
            self.app.update_cps_display(self.total_auto_clicks_per_second)

        self.cps_event = threading.Event()

        # Begin cps thread
        self.cps_thread = threading.Thread(
            target=self.add_cookies_every_second
        )
        self.cps_thread.start()
        self.cps_event.set()

    def create_auto_clickers(self):
        """Populate the `auto_clickers` dictionary."""
        ac_1 = AutoClickers('Dough Roller', 0.1, 50, 0)
        ac_2 = AutoClickers('Secret Recipe', 0.5, 100, 0)
        ac_3 = AutoClickers('Small Bussiness', 2.0, 200, 0)

        self.auto_clickers = self.convert_to_dictionary_format(
            [ac_1, ac_2, ac_3]
        )

    def convert_to_dictionary_format(self, auto_clickers):
        """Convert the list of auto_clickers to a dictionary."""
        the_dict = {au_c.name: au_c for au_c in auto_clickers}
        return the_dict

    def buy_auto_clicker(self, name):
        """Allow user to purchase `AutoClickers`.
        
        If the user has sufficient funds, the auto clicker will be purchased,
        `cookies` subtracted, and displays updated accordingly.

        If the user does not have sufficient funds, the user will be alerted so.

        Parameter
        ---------
        name : str
        """
        if self.auto_clickers[name].is_affordable(self.cookies):
            self.auto_clickers[name].buy(self.cookies)
            self.cookies -= self.auto_clickers[name].unit_price
            self.app.update_cookie_number_display(self.cookies)
            self.app.update_cps_display(self.total_auto_clicks_per_second)
        else:
            if self.app is not None:
                self.app.alert_user('You do not have enough cookies!')

    def player_click(self):
        """Function to process the user clicking the main button."""
        self.cookies += 1
        self.app.update_cookie_number_display(self.cookies)

    @property
    def total_auto_clicks_per_second(self):
        """Returns the total cps."""
        return sum(
            au_c.total_output
            for au_c in self.auto_clickers.values()
        )

    def add_cookies_every_second(self):
        """Adds cookies from the auto cps every second.
        
        This function makes use of the `cps_event`.
        It first waits for the event to be set, and once done so,
        it will add `total_auto_clicks_per_second` to `cookies`,
        whilst updating the cookie number display.
        """
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
