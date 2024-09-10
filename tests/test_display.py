"""
test display module
"""

import os
import unittest


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


if __name__ == '__main__':
    display_img()
