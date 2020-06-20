from dataclasses import dataclass


@dataclass
class AutoClickers:
    """
    A dataclass instance to hold the user's auto clickers.

    Attributes
    ----------
    name : str
    cookies_per_second : float
    unit_price : float
    player_quantity : int

    Methods
    -------
    is_affordable(player_money)
    buy()
    total_output()

    """
    name: str
    cookies_per_second: float
    unit_price: float
    player_quantity: int

    def is_affordable(self, player_money):
        """Returns a bool."""
        if player_money >= self.unit_price:
            return True

        return False

    def buy(self, player_money):
        """Increases the `player_quantity` by one."""
        self.player_quantity += 1

    @property
    def total_output(self):
        """Returns the `player_quantity` multiplied by `cookies_per_second`."""
        return self.player_quantity * self.cookies_per_second
