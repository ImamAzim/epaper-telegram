import logging


from waveshare_touch_epaper.touch_screen import GT1151
from epaper_telegram.models.mocks import GT1151Mock
from epaper_telegram.models.img_creators import DrawTool, OnlineImageDownloader
from epaper_telegram.models.display import Displayer
from epaper_telegram.models.online_tools import OnlineImg


class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self, mock_mode=False):
        if mock_mode:
            self._GT = GT1151Mock
        else:
            self._GT = GT1151
        self._mock_mode = mock_mode
        if mock_mode:
            self._online_img_tool = OnlineImg(mock_mode=mock_mode)
        else:
            logging.debug('TODO: get credentials')
            credentials = dict()
            self._online_img_tool = OnlineImg(**credentials)

    def start(self):
        """method to start the app.
        :returns: TODO

        """

        logging.info('start')
        logging.debug('debug mode')

        try:
            with (
                    self._GT() as gt,
                    Displayer(mock_mode=self._mock_mode) as displayer,
                    ):
                with OnlineImageDownloader(displayer, self._online_img_tool) as online_image_downloader:
                    while True:
                        logging.info('home')
                        gt.wait_for_gesture()
                        logging.info('open draw mode...')
                        with DrawTool(displayer) as draw_tool:
                            to_continue = True
                            while to_continue:
                                coordinates = gt.input()
                                to_continue, img = draw_tool.point_to(*coordinates)
                            if img is not None:
                                online_image_downloader.upload(img)
                        online_image_downloader.display_now()
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


if __name__ == '__main__':
    pass
