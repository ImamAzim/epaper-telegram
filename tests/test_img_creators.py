import logging
import unittest
import time


from epaper_telegram.models.img_creators import DrawTool
from epaper_telegram.models.display import Displayer


class TestMyClass(unittest.TestCase):

    """all test concerning my class. """

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

    # def test_point_to(self):
        # pass

    def test_clear_img(self):
        self.draw_tool.clear_img()


def draw_tool():
    logging.basicConfig(level=logging.INFO)
    with Displayer(mock_mode=True) as displayer:
        with DrawTool(displayer) as draw_tool:
            draw_tool.clear_img()
            # time.sleep(2)
            # draw_tool.point_to(125, 61, 9)
            # time.sleep(2)


if __name__ == "__main__":
    draw_tool()
