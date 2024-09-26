import logging
import unittest
import time


from PIL import Image


from epaper_telegram.models.img_creators import DrawTool, OnlineImageDownloader
from epaper_telegram.models.display import Displayer


class TestDrawToo(unittest.TestCase):

    """all test concerning Draw Tool. """
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
        y = int(self._IMG_HEIGHT * 1/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, False)
        self.assertIsInstance(img, Image.Image)
        # erase button
        y = int(self._IMG_HEIGHT * 3/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, True)
        # cancel button
        y = int(self._IMG_HEIGHT * 5/6)
        to_continue, img = self.draw_tool.point_to(x, y, 1)
        self.assertIs(to_continue, False)
        self.assertIs(img, None)

    def test_clear_img(self):
        self.draw_tool.clear_img()


class TestOnlineImg(unittest.TestCase):

    """all test concerning Online Image Downloader. """
    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122

    @classmethod
    def setUpClass(cls):
        credentials = dict(
                jabber_id=None,
                password=None,
                )
        cls.displayer = Displayer(mock_mode=True)
        cls.displayer.start()
        cls.online_img_down = OnlineImageDownloader(
                cls.displayer,
                credentials,
                corresp_jid=None,
                mock_mode=True,
                )
        cls.online_img_down.start()

    @classmethod
    def tearDownClass(cls):
        cls.online_img_down.terminate()
        cls.displayer.terminate()

    def test_display_now(self):
        self.online_img_down.display_now()

    def test_upload(self):
        width = 250
        height = 122
        img = Image.new('1', (width, height), 255)
        t = self.online_img_down.upload(img)
        t.join()


def draw_tool():
    logging.basicConfig(level=logging.INFO)
    with Displayer(mock_mode=True) as displayer:
        with DrawTool(displayer) as draw_tool:
            time.sleep(2)
            draw_tool.point_to(125, 61, 9)
            time.sleep(2)


def online_image_downloader():
    logging.basicConfig(level=logging.DEBUG)
    with Displayer(mock_mode=True) as displayer:
        with OnlineImageDownloader(
                displayer,
                dict(jabber_id='me', password='pass'),
                corresp_jid=None,
                mock_mode=True,
                ):
            time.sleep(5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    online_image_downloader()
