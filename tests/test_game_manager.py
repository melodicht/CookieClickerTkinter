import unittest
from unittest import mock

from AutoClickers import AutoClickers
from GameManager import GameManager


class TestGameManager(unittest.TestCase):
    @mock.patch('GameManager.GameManager.app')
    def setUp(self, mock_gm_app):
        self.auto_clicker_1 = AutoClickers('Factory', 5.0, 15.0, 0)
        self.auto_clicker_2 = AutoClickers('Farm', 10.0, 50.0, 3)
        self.auto_clicker_3 = AutoClickers('House', 20.0, 100.0, 5)
        self.game_manager = GameManager(
            auto_clickers=[
                self.auto_clicker_1, self.auto_clicker_2, self.auto_clicker_3
            ]
        )
        self.game_manager.app = mock_gm_app

    def tearDown(self):
        self.game_manager.cps_event.clear()
        self.game_manager.cps_thread.join()

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

    @mock.patch('GameManager.GameManager.app')
    def test_buy_one_auto_clicker_with_insufficient_funds(self,
                                                          mock_gm_app):
        self.game_manager.cookies = 0
        self.game_manager.app = mock_gm_app
        self.game_manager.buy_auto_clicker('Factory')
        self.assertEqual(mock_gm_app.alert_user.call_count, 1)

    @mock.patch('GameManager.GameManager.app')
    def test_update_cookie_number_display_with_buy(self, mock_gm_app):
        self.game_manager.app = mock_gm_app
        self.game_manager.cookies = 150

        self.game_manager.buy_auto_clicker('Factory')
        self.assertEqual(mock_gm_app.update_cookie_number_display.call_count,
                         1)
        mock_gm_app.update_cookie_number_display.assert_called_with(135)

        self.game_manager.buy_auto_clicker('Farm')
        self.assertEqual(mock_gm_app.update_cookie_number_display.call_count,
                         2)
        mock_gm_app.update_cookie_number_display.assert_called_with(85)

        self.game_manager.cookies = 110
        self.game_manager.buy_auto_clicker('House')
        self.assertEqual(mock_gm_app.update_cookie_number_display.call_count,
                         3)
        mock_gm_app.update_cookie_number_display.assert_called_with(10)

    @mock.patch('GameManager.GameManager.app')
    def test_update_cookie_number_display_with_click(self, mock_gm_app):
        self.game_manager.app = mock_gm_app
        self.game_manager.cookies = 100

        self.game_manager.player_click()
        self.assertEqual(mock_gm_app.update_cookie_number_display.call_count,
                         1)
        mock_gm_app.update_cookie_number_display.assert_called_with(101)

        self.game_manager.player_click()
        self.assertEqual(mock_gm_app.update_cookie_number_display.call_count,
                         2)
        mock_gm_app.update_cookie_number_display.assert_called_with(102)

    def test_buy_auto_clicker_actually_buys(self):
        with mock.patch.object(self.game_manager, 'auto_clickers') as mock_ac:
            self.game_manager.cookies = 150
            mock_ac['Factory'].is_affordable.return_value = True
            self.game_manager.buy_auto_clicker('Factory')
            self.assertEqual(mock_ac['Factory'].buy.call_count, 1)
            mock_ac['Factory'].buy.assert_called_with(150)

            # If not enough, don't buy
            self.game_manager.cookies = 0
            mock_ac['Factory'].is_affordable.return_value = False
            self.game_manager.buy_auto_clicker('Factory')
            self.assertEqual(mock_ac['Factory'].buy.call_count, 1)
