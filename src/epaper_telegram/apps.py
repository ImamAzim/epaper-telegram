import logging


from epaper_telegram.models.touch_epaper import EpdTouch2In13

class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self):
        epd_touch = EpdTouch2In13()

    def start(self):
        """method to start the app.
        :returns: TODO

        """
        logging.info('start')
        logging.debug('debug mode')


if __name__ == '__main__':
    pass
