import pickle
from cryptography.fernet import Fernet
import secrets
import string
import datetime
import os
import getpass
import logging


from epaper_telegram import DATA_DIR_PATH


class ImageTransferBot(object):

    """bot that will receive or send img on jabber"""

    def __init__(self, msg_receive_event, jid='', password='', corresp_jid=''):
        """TODO: to be defined. """
        pass

    def send_img(self, img):
        """send an img file to the correspondant

        :img: TODO
        :returns: TODO

        """
        logging.debug('TODO: send img with xmpp')


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
        credentials = self._create_new_cred()

    def _decrypt_password(self, encrypted_pass, key):
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
        with open (path, 'wb') as keyfile:
            pickle.dump(key.decode(), keyfile)

    def _load_key(self):
        path = os.path.join(DATA_DIR_PATH, self._KEY_FILE)
        with open (path, 'rb') as keyfile:
            key = pickle.load(keyfile).encode()
        return key



if __name__ == '__main__':
    credential_handler = CredentialsHandler()
    credentials, key = credential_handler._create_new_cred()
    print(key)
    credential_handler._save_key(key)
    key = credential_handler._load_key()
    print(key)
