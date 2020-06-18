import unittest
from GameManager import GameManager
from AutoClickers import AutoClickers


class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.auto_clicker_1 = AutoClickers('Factory', 5.0, 15.0, 0)
        self.auto_clicker_2 = AutoClickers('Farm', 10.0, 50.0, 3)
        self.auto_clicker_3 = AutoClickers('House', 20.0, 100.0, 5)
        self.game_manager = GameManager(
            auto_clickers=[
                self.auto_clicker_1, self.auto_clicker_2, self.auto_clicker_3
            ]
        )

    def test_convert_to_dictionary_format(self):
        auto_clicker_dict = {
            'Factory': self.auto_clicker_1,
            'Farm': self.auto_clicker_2,
            'House': self.auto_clicker_3
        }
        self.assertEqual(self.game_manager.auto_clickers, auto_clicker_dict)

    def test_total_auto_clicks_per_second(self):
        self.assertEqual(
            self.game_manager.total_auto_clicks_per_second, 130.0
        )

    def test_player_cookies(self):
        self.game_manager.cookies = 150.0
        self.assertEqual(self.game_manager.cookies, 150.0)

        self.game_manager.buy_auto_clicker('Factory')
        self.assertEqual(self.game_manager.cookies, 135.0)

    def test_buy_one_auto_clickers(self):
        self.game_manager.cookies = 150.0

        self.game_manager.buy_auto_clicker('Factory')
        self.assertEqual(self.game_manager.cookies, 135.0)
        self.assertEqual(
            self.game_manager.auto_clickers['Factory'].player_quantity, 1
        )

        self.game_manager.buy_auto_clicker('Farm')
        self.assertEqual(self.game_manager.cookies, 85.0)
        self.assertEqual(
            self.game_manager.auto_clickers['Farm'].player_quantity, 4
        )