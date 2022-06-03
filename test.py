from ship import Ship
from alien_invasion import AlienInvasion
import unittest
import time

class TestShip(unittest.TestCase):
    def test_center_ship(self):
        game = AlienInvasion()
        ship = Ship(game)
        ship.center_ship()
        game._update_screen()
        time.sleep(10)
 
 
if __name__ == '__main__':
    unittest.main()
