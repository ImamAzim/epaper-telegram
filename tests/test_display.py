"""
test display module
"""

import unittest


from PIL import Image, ImageDraw


from epaper_telegram.models.display import Displayer


class TestMyClass(unittest.TestCase):

    """all test concerning my class. """

    @classmethod
    def setUpClass(cls):
        pass

    pass


""" script tests """


def display_img():
    displayer = Displayer()
    img = Image.new('1', (250, 122), 255)
    draw = ImageDraw.Draw(img)
    draw.text((8, 12), 'hello world', fill=255)
    displayer.display_img(img)


if __name__ == '__main__':
    display_img()
