import logging


from waveshare_touch_epaper import gt1151, epd2in13_V4


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


if __name__ == '__main__':
    pass
