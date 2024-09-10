"""
test display module
"""

import unittest
from threading import RLock


from PIL import Image, ImageDraw


from epaper_telegram.models.display import Displayer


class TestMyClass(unittest.TestCase):

    """all test concerning my class. """

    @classmethod
    def setUpClass(cls):
        cls.displayer = Displayer()

    def test_lock(self):
        rlock = self.displayer
        self.assertIsInstance(rlock, RLock)


""" script tests """


def display_img():
    displayer = Displayer()
    img = Image.new('1', (250, 122), 255)
    draw = ImageDraw.Draw(img)
    draw.text((8, 12), 'hello world', fill=255)
    displayer.display_img(img)


if __name__ == '__main__':
    display_img()
