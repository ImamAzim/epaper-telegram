import argparse
import logging


class epaper_telegram_app(object):

    """app to launch the main app of the project"""

    def __init__(self):
        pass

    def start(self):
        """method to start the app.
        :returns: TODO

        """
        logging.info('start')
        logging.debug('debug mode')


def launch_epaper_telegram():
    """lauch the main app. you can add verbose mode to debug
    :returns: TODO

    """
    parser = argparse.ArgumentParser(
            prog='epaper telegram',
            description='send and receive message on epaper with a rasperry pi',
            )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--logfile', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    if args.logfile:
        filename = 'epaper-telgram.log'
        logging.basicConfig(
                filename=filename,
                encoding='utf-8',
                format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
                datefmt="%Y.%m.%d %H:%M:%S",
                level=level,
                )
    else:
        logging.basicConfig(
                encoding='utf-8',
                format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
                datefmt="%Y.%m.%d %H:%M:%S",
                level=level,
                )
    app = epaper_telegram_app()
    app.start()


if __name__ == '__main__':
    pass
