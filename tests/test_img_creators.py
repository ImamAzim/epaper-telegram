import logging
import unittest
import time


from PIL import Image


from epaper_telegram.models.img_creators import DrawTool
from epaper_telegram.models.display import Displayer


class TestMyClass(unittest.TestCase):

    """all test concerning my class. """
    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122

    @classmethod
    def setUpClass(cls):
        cls.displayer = Displayer(mock_mode=True)
        cls.displayer.start()
        cls.draw_tool = DrawTool(cls.displayer)
        cls.draw_tool.start()

    @classmethod
    def tearDownClass(cls):
        cls.draw_tool.terminate()
        cls.displayer.terminate()

    def test_point_to(self):
        center = self._IMG_WIDTH / 2, self._IMG_HEIGHT / 2
        to_continue, img = self.draw_tool.point_to(*center, 1)
        self.assertIs(to_continue, True)
        x = 0
        # send button
        y = self._IMG_HEIGHT * int(1/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, False)
        self.assertIsInstance(img, Image.Image)
        # erase button
        y = self._IMG_HEIGHT * int(3/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, True)
        # cancel button
        y = self._IMG_HEIGHT * int(5/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, False)
        self.assertIs(img, None)

    def test_clear_img(self):
        self.draw_tool.clear_img()


def draw_tool():
    logging.basicConfig(level=logging.INFO)
    with Displayer(mock_mode=True) as displayer:
        with DrawTool(displayer) as draw_tool:
            time.sleep(2)
            draw_tool.point_to(125, 61, 9)
            time.sleep(2)


if __name__ == "__main__":
    draw_tool()
