import logging
import time


from waveshare_touch_epaper.touch_screen import GT1151

class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self):
        pass

    def start(self):
        """method to start the app.
        :returns: TODO

        """
        logging.info('start')
        logging.debug('debug mode')

        thread_hello.start()

        try:
            while True:
                logging.info('home')
                with GT1151() as gt:
                    gt.wait_for_gesture()
                logging.info('open draw mode...')
                _draw_mode()
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


def _say_hello():
    print('hello')
    time.sleep(1)

thread_hello = Thread(target=_say_hello)

def _draw_mode():
    with GT1151() as gt:
        gt.input()


if __name__ == '__main__':
    pass
