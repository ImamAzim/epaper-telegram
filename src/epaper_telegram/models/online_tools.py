import logging


from PIL import Image


class OnlineImgError(Exception):
    pass


class OnlineImg(object):

    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122

    """manage online img"""
    def __init__(self,
            upload_url=None,
            upload_username=None,
            upload_password=None,
            download_username=None,
            download_password=None,
            mock_mode=False,
            ):
        """TODO: to be defined.

        :upload_url: TODO
        :upload_username: TODO
        :upload_password: TODO
        :download_url: TODO
        :download_username: TODO
        :download_password: TODO
        :mock_mode: TODO
        :: TODO

        """
        self._upload_url = upload_url
        self._upload_username = upload_username
        self._upload_password = upload_password
        self._download_url = download_url
        self._download_username = download_username
        self._download_password = download_password
        self._mock_mode = mock_mode

    def upload(self, img):
        """upload img on the cloud

        :img: PIL img object

        """
        pass

    def download(self):
        """download img from the cloud
        :returns: PIL Image

        """
        if self._mock_mode:
            img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        else:
            logging.debug('TODO: download img')
        return img

    def get_hash(self):
        """get the hash function of online img to verify if a new img is available
        :returns: hash

        """
        if self._mock_mode:
            img_hash = 1
        else:
            logging.debug('TODO: get hash of online img')
        return img_hash
