import logging
import time
from threading import Thread


from waveshare_touch_epaper.touch_screen import GT1151
from epaper_telegram.models.mocks import GT1151Mock


class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self, mock_mode=False):
        if mock_mode:
            self._GT = GT1151Mock
        else:
            self._GT = GT1151

    def start(self):
        """method to start the app.
        :returns: TODO

        """

        logging.info('start')
        logging.debug('debug mode')


        try:
            with self._GT() as gt:
                while True:
                    logging.info('home')
                    gt.wait_for_gesture()
                    logging.info('open draw mode...')
                    gt.input()
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


if __name__ == '__main__':
    pass
