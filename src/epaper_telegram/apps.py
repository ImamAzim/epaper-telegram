import logging
import os
import configparser


from waveshare_touch_epaper.touch_screen import GT1151
from epaper_telegram.models.mocks import GT1151Mock
from epaper_telegram.models.img_creators import DrawTool, OnlineImageDownloader
from epaper_telegram.models.display import Displayer
from epaper_telegram.models.xmpp import CredentialsHandler, CredentialsHandlerError, RegisterBot
from epaper_telegram import DATA_DIR_PATH, ACCOUNTS_CREATED_FILE, CORRESP_JID_FILE


class EpaperTelgramApp(object):

    """app to launch the main app of the project"""

    def __init__(self, mock_mode=False):
        if mock_mode:
            self._GT = GT1151Mock
        else:
            self._GT = GT1151
        self._mock_mode = mock_mode
        with open(CORRESP_JID_FILE, 'r') as myfile:
            self._corresp_jid = myfile.read()
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
            with (
                    self._GT() as gt,
                    Displayer(mock_mode=self._mock_mode) as displayer,
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
                                to_continue, img = draw_tool.point_to(*coordinates)
                            if img is not None:
                                online_image_downloader.upload(img)
                        online_image_downloader.display_now()
        except KeyboardInterrupt:
            logging.info('app stopped by keyboard interrupt')

class ConfigEpaperTelegram(object):

    """an app to configure epaper telegram"""

    def __init__(self):
        pass

    def start(self):
        """run the config app in a terminal
        :returns: TODO

        """
        user_jid = self._check_account()

    def _check_account(self):
        credential_handler = CredentialsHandler()
        try:
            credentials = credential_handler.load_credentials()
        except FileNotFoundError:
            credential_handler.create_and_save_new_cred(force=True)
            credentials = credential_handler.load_credentials()

        path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
        config = configparser.ConfigParser()
        config.read(path)
        if credentials['jabber_id'] not in config:
            print('register a new account...')
            # register_bot = RegisterBot(**credentials)
            # register_bot.connect()
            # register_bot.process(forever=False)

        user_jid = credentials['jabber_id']
        return user_jid


if __name__ == '__main__':
    pass
