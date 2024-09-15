import logging
import time
from threading import Thread


from waveshare_touch_epaper.touch_screen import GT1151
from epaper_telegram.models.mocks import GT1151Mock
from epaper_telegram.models.img_creators import DrawTool
from epaper_telegram.models.display import Displayer


class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self, mock_mode=False):
        if mock_mode:
            self._GT = GT1151Mock
        else:
            self._GT = GT1151
        self._mock_mode = mock_mode

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
                logging.info('TODO: start thread download img and display')
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
                            logging.info('TODO: upload image')
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


if __name__ == '__main__':
    pass
