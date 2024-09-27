import argparse
import logging


from epaper_telegram.apps import EpaperTelgramApp, ConfigEpaperTelegram


def launch_epaper_telegram():
    """lauch the main app. you can add verbose mode to debug
    :returns: TODO

    """

    parser = argparse.ArgumentParser(
            prog='epaper telegram daemon',
            description='send and receive message on epaper with a rasperry pi',
            epilog='do no lauch this daemon manually, it will be used by crontab'
            )
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--logfile', action='store_true')
    parser.add_argument('-m', '--mock', action='store_true')
    parser.add_argument("-c", "--correspondant", dest="corresp_jid",
                        help="JID to send the message to")
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

    app = EpaperTelgramApp(
            corresp_jid=args.corresp_jid,
            mock_mode=args.mock,
            )
    app.start()


def launch_epaper_config():
    """launch the config app in a terminal

    """
    parser = argparse.ArgumentParser(
            prog='epaper telegram',
            description='use this to configure and activate the epaper telegram daemon',
            )
    app = ConfigEpaperTelegram()
    app.start()


if __name__ == '__main__':
    pass
