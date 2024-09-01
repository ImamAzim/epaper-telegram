import logging


from epaper_telegram.models.touch_epaper import GT1151

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

        with GT1151() as gt:
            x, y, s = gt.input()
        logging.info('touch detected at %s, %s, %s', x, y, s)
        logging.info('open draw mode...')


if __name__ == '__main__':
    pass
