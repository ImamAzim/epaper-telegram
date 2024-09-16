class OnlineImg(object):

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
        pass

    def get_hash(self):
        """get the hash function of online img to verify if a new img is available
        :returns: hash

        """
        pass

class OnlineImage(object):

    """manage online img on the cloud"""

