import configparser
import pickle
from cryptography.fernet import Fernet
import secrets
import string
import datetime
import os
import getpass
import logging


from epaper_telegram import DATA_DIR_PATH, ACCOUNTS_CREATED_FILE


class ImageTransferBot(object):

    """bot that will receive or send img on jabber"""

    def __init__(self, msg_receive_event, jabber_id='', password='', corresp_jid=''):
        path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
        config = configparser.ConfigParser()
        config.read(path)
        if jabber_id not in config:
            logging.info('TODO: create an account')

    def send_img(self, img):
        """send an img file to the correspondant

        :img: TODO
        :returns: TODO

        """
        logging.debug('TODO: send img with xmpp')

class CredentialsHandlerError(Exception):
    pass


class CredentialsHandler(object):

    """a help to create, save and reload credentials for jabber account"""

    _DOMAIN = '@jabber.fr'
    _CRED_FILE = 'cred.ini'
    _KEY_FILE = '.key'

    def __init__(self):
        pass

    def create_and_save_new_cred(self):
        """will create new credentials. uses the user name, host and current day

        """
        credentials, key = self._create_new_cred()
        self._save_key(key)
        self._save_credentials(credentials)
        logging.info('new credentials created')

    def load_credentials(self):
        """load credentials from encrypted file
        :returns: credentials

        """
        key = self._load_key()
        credentials = self._load_credentials()
        password = self._decrypt_password(
                credentials['encrypted_password'],
                key,
                )
        credentials['password'] = password
        del credentials['encrypted_password']
        logging.info('credentials loaded')
        return credentials

    def _decrypt_password(self, encrypted_password, key):
        f = Fernet(key)
        password = f.decrypt(encrypted_password.encode()).decode()
        return password
        del f

    def _encrypt_password(self, password, key):
        f = Fernet(key)
        encrypted_pass= f.encrypt(password.encode()).decode()
        del f
        return encrypted_pass

    def _gen_password(self):
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        return password

    def _create_new_cred(self):
        user = getpass.getuser()
        host = os.uname()[1]
        date = datetime.date.today()
        username = f'{user}_{host}_{date}_BOT'
        jabber_id = username + self._DOMAIN

        password = self._gen_password()
        key = Fernet.generate_key()
        encrypted_password = self._encrypt_password(password, key)

        credentials = dict(
                jabber_id=jabber_id,
                encrypted_password=encrypted_password,
                )
        return credentials, key

    def _save_key(self, key):
        path = os.path.join(DATA_DIR_PATH, self._KEY_FILE)
        if os.path.exists(path):
            msg = 'a key file already existsü'
            raise CredentialsHandlerError(msg)
        with open (path, 'wb') as keyfile:
            pickle.dump(key.decode(), keyfile)

    def _load_key(self):
        path = os.path.join(DATA_DIR_PATH, self._KEY_FILE)
        with open (path, 'rb') as keyfile:
            key = pickle.load(keyfile).encode()
        return key

    def _save_credentials(self, credentials):
        path = os.path.join(DATA_DIR_PATH, self._CRED_FILE)
        if os.path.exists(path):
            msg = 'a credential file already exists'
            raise CredentialsHandlerError(msg)
        config = configparser.ConfigParser()
        config['jabber'] = credentials
        with open(path, 'w') as configfile:
            config.write(configfile)

    def _load_credentials(self):
        path = os.path.join(DATA_DIR_PATH, self._CRED_FILE)
        config = configparser.ConfigParser()
        config.read(path)
        credentials = dict(config['jabber'])
        return credentials


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    credential_handler = CredentialsHandler()
    try:
        credentials = credential_handler.load_credentials()
    except FileNotFoundError:
        credential_handler.create_and_save_new_cred()
        credentials = credential_handler.load_credentials()
    image_transfer_bot = ImageTransferBot(**credentials, msg_receive_event=None)
