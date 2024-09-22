import unittest


from PIL import Image


from epaper_telegram.models.tools import ImgConvertor


class TestImgConvertor(unittest.TestCase):

    """all test concerning my ImgConvertor. """

    @classmethod
    def setUpClass(cls):
        cls.img_convertor = ImgConvertor()

    def test_img2str(self):
        img = Image.new('1', (200, 100, 255))
        img_str = self.img_convertor.img2str(img)
        self.assertIsInstance(img_str, Image.Image)
