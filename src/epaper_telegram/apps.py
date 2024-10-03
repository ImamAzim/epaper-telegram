import logging
import configparser


from varboxes import VarBox
from waveshare_touch_epaper import touchscreen_models
from waveshare_touch_epaper.touch_screen import BaseTouchScreen


from epaper_telegram.models.img_creators import DrawTool, OnlineImageDownloader
from epaper_telegram.models.display import Displayer
from epaper_telegram.models.xmpp import CredentialsHandler, RegisterBot
from epaper_telegram.views import ConfigureMenu
from epaper_telegram import ACCOUNTS_CREATED_FILE, APP_NAME


class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self):

        vb = VarBox(APP_NAME)
        try:
            self._corresp_jid = vb.corresp_jid
        except AttributeError:
            logging.warning(
                    (
                        'no correspondant found! '
                        'the app will run but cannot send and receive msg'
                        ),
                    )
            self._corresp_jid = ''
        try:
            self._touch_model_name = vb.touch_model_name
        except AttributeError:
            logging.warning(
                    'no touchscreen model define. Use mock mode.'
                    )
            self._touch_model_name = 'GT1151Mock'
        try:
            self._epaper_model_name = vb.epaper_model_name
        except AttributeError:
            logging.warning(
                    'no epaper model defined. Use mock mode.'
                    )
            self._epaper_model_name = 'EPD2in13Mock'

        credential_handler = CredentialsHandler()
        credentials = credential_handler.load_credentials()
        self._credentials = credentials

    def start(self):
        """method to start the app.
        :returns: TODO

        """

        logging.info('start')
        logging.debug('debug mode')

        try:
            gt: BaseTouchScreen
            with (
                    touchscreen_models[self._touch_model_name]() as gt,
                    Displayer(self._epaper_model_name) as displayer,
                    ):
                with OnlineImageDownloader(
                        displayer,
                        self._credentials,
                        corresp_jid=self._corresp_jid,
                        ) as online_image_downloader:
                    while True:
                        logging.info('home')
                        gt.wait_for_gesture()
                        logging.info('open draw mode...')
                        with DrawTool(displayer) as draw_tool:
                            to_continue = True
                            while to_continue:
                                coordinates = gt.input()
                                to_continue, img = draw_tool.point_to(
                                        *coordinates,
                                        )
                            if img is not None:
                                online_image_downloader.upload(img)
                        online_image_downloader.display_now()
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')


class ConfigEpaperTelegram(object):

    """an app to configure epaper telegram"""

    def __init__(self):
        self._view = ConfigureMenu()

    def start(self):
        """run the config app in a terminal
        :returns: TODO

        """
        user_jid = self._check_account()
        self._view.start(user_jid)

    def _check_account(self):
        credential_handler = CredentialsHandler()
        try:
            credentials = credential_handler.load_credentials()
        except FileNotFoundError:
            credential_handler.create_and_save_new_cred(force=True)
            credentials = credential_handler.load_credentials()

        path = ACCOUNTS_CREATED_FILE
        config = configparser.ConfigParser()
        config.read(path)
        if credentials['jabber_id'] not in config:
            print('register a new account...')
            register_bot = RegisterBot(**credentials)
            register_bot.connect()
            register_bot.process(forever=False)

        user_jid = credentials['jabber_id']
        return user_jid


if __name__ == '__main__':
    pass
