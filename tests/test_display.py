"""
test display module
"""

import unittest
from threading import RLock
import time


from PIL import Image, ImageDraw


from epaper_telegram.models.display import Displayer


class TestMyClass(unittest.TestCase):

    """all test concerning my class. """

    @classmethod
    def setUpClass(cls):
        cls.displayer = Displayer()

    @classmethod
    def tearDownClass(cls):
        cls.displayer.terminate()

    def test_lock(self):
        rlock = self.displayer.rlock
        self.assertIsInstance(rlock, type(RLock()))

    def test_wait(self):
        self.displayer.wait_for_ready()


""" script tests """


def display_img():
    with Displayer() as displayer:
        img = Image.new('1', (250, 122), 255)
        draw = ImageDraw.Draw(img)
        draw.text((8, 12), 'hello world', fill=0)
        displayer.display_img(img, sleep_after=False)
        time.sleep(3)
        draw.text((8, 61), 'zzz...', fill=0)
        displayer.display_img(img)
        displayer.wait_for_ready()
        time.sleep(3)


if __name__ == '__main__':
    display_img()
