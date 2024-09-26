import time
import logging


from PIL import Image, ImageDraw


from epaper_telegram.models.xmpp import CredentialsHandler
from epaper_telegram.models.img_creators import OnlineImageDownloader
from epaper_telegram.models.display import Displayer


logging.basicConfig(level=logging.INFO)

credential_handler = CredentialsHandler()
try:
    credentials = credential_handler.load_credentials()
except FileNotFoundError:
    credential_handler.create_and_save_new_cred()
    credentials = credential_handler.load_credentials()


def send_while_check():
    with Displayer(True) as displayer:
        with OnlineImageDownloader(
                displayer,
                credentials,
                corresp_jid=credentials['jabber_id'],
                # corresp_jid='nobody',
                mock_mode=True
                ) as online_image_downloader:
            time.sleep(1)
            img = Image.new('1', (200, 100), 255)
            draw = ImageDraw.Draw(img)
            draw.text((100, 50), 'salut!')
            online_image_downloader.upload(img)


if __name__ == '__main__':
    send_while_check()
