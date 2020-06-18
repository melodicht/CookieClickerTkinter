from dataclasses import dataclass


@dataclass
class AutoClickers:
    name: str
    cookies_per_second: float
    unit_price: float
    player_quantity: int

    def is_affordable(self, player_money):
        if player_money >= self.unit_price:
            return True

        return False

    def buy(self, player_money):
        self.player_quantity += 1

    @property
    def total_output(self):
        return self.player_quantity * self.cookies_per_second
