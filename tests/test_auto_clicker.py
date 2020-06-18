import unittest

from AutoClickers import AutoClickers


class TestAutoClicker(unittest.TestCase):
    def setUp(self):
        self.auto_clicker_1 = AutoClickers('Factory', 5.0, 15.0, 0)
        self.auto_clicker_2 = AutoClickers('Farm', 5.0, 15.0, 3)

    def test_if_affordable(self):
        player_money = 10.0
        self.assertFalse(self.auto_clicker_1.is_affordable(player_money))
        player_money = 20.0
        self.assertTrue(self.auto_clicker_1.is_affordable(player_money))

    def test_buy(self):
        player_money = 30.0
        self.auto_clicker_1.buy(player_money)
        self.assertEqual(self.auto_clicker_1.player_quantity, 1)
        self.auto_clicker_2.buy(player_money)
        self.assertEqual(self.auto_clicker_2.player_quantity, 4)

    def test_total_output(self):
        self.assertEqual(self.auto_clicker_1.total_output, 0)
        self.assertEqual(self.auto_clicker_2.total_output, 15.0)

        self.auto_clicker_1.buy(30.0)
        self.assertEqual(self.auto_clicker_1.total_output, 5.0)

    def test_name(self):
        self.assertEqual(self.auto_clicker_1.name, 'Factory')
        self.assertEqual(self.auto_clicker_2.name, 'Farm')


if __name__ == '__main__':
    unittest.main()
