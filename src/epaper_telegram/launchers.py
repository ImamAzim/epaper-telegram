import argparse
import logging


from epaper_telegram.apps import EpaperTelgramApp


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
    parser.add_argument('-m', '--mock', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging_config_kwargs = dict(
            encoding='utf-8',
            format="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
            level=level,
            )
    if args.logfile:
        logging_config_kwargs['filename'] = 'epaper-telegram.log'
    logging.basicConfig(**logging_config_kwargs)

    app = EpaperTelgramApp(mock_mode=args.mock)
    app.start()


if __name__ == '__main__':
    pass
