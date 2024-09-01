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

        try:
            with GT1151() as gt:
                while True:
                    logging.info('main mode')
                    gt.input()
                    logging.info('touch detected')
                    logging.info('open draw mode...')
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


if __name__ == '__main__':
    pass
