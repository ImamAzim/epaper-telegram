import asyncio
import threading
import configparser
import pickle
from cryptography.fernet import Fernet
import secrets
import string
import datetime
import os
import getpass
import logging
import urllib.request
from urllib.error import URLError


import slixmpp
from PIL import Image
from slixmpp.exceptions import IqTimeout, IqError


from epaper_telegram import DATA_DIR_PATH, ACCOUNTS_CREATED_FILE


class ImageTransferBotError(Exception):
    pass


class ReceiverBot(slixmpp.ClientXMPP):

    """
    a bot to save received img or to send one
    """

    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122
    _IMG_FILE_PATH = os.path.join(DATA_DIR_PATH, 'received_img.bmp')

    def __init__(
            self,
            jabber_id,
            password,
            corresp_jid,
            ):
        slixmpp.ClientXMPP.__init__(self, jabber_id, password)

        self.add_event_handler("session_start", self._start)
        self.add_event_handler("message", self._save_img)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping

        asyncio.set_event_loop(self.loop)
        self._correspondant = corresp_jid.lower()

        try:
            self._img = Image.open(self._IMG_FILE_PATH)
        except FileNotFoundError:
            self._img = None

    @property
    def img(self):
        if self._img is not None:
            return self._img
        else:
            msg = 'there is not last version of received img'
            logging.error(msg)
            raise ImageTransferBotError(msg)

    def wait_for_msg(self):
        """block until a new img is received and save it to the disk
        :returns: TODO

        """
        self.connect()
        self.loop.run_until_complete(self.disconnected)

    def stop_waiting(self):
        """stop the blocking wait even if there is no updated img

        """
        self.loop.call_soon_threadsafe(self.disconnect)

    async def _start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        logging.debug('start: send presence and get roster')
        self.send_presence()
        await self.get_roster()

    def _save_img(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        logging.info('received msg')
        if msg['type'] in ('chat', 'normal'):
            jid = slixmpp.JID(msg['from']).bare
            if self._correspondant == jid:
                url = msg['body']
                try:
                    urllib.request.urlretrieve(url, self._IMG_FILE_PATH)
                    logging.info('img saved to disk')
                except URLError:
                    logging.warning(
                            'could not download the img.',
                            'maybe the message did not contain an img url')
                except ValueError:
                    logging.warning(
                            'could not read the url of the msg'
                            )
                else:
                    img = Image.open(self._IMG_FILE_PATH)
                    self._img = img
                    self.disconnect()
            else:
                logging.warning('msg is was sent by %s', jid)
        else:
            logging.warning('msg is %s', msg['type'])


class SenderBot(slixmpp.ClientXMPP):

    """
    a bot to save received img or to send one
    """

    _IMG_FILE_PATH = os.path.join(DATA_DIR_PATH, 'to_send.bmp')

    def __init__(
            self,
            jabber_id,
            password,
            corresp_jid,
            ):
        slixmpp.ClientXMPP.__init__(self, jabber_id, password)

        self._correspondant = corresp_jid

        self.add_event_handler("session_start", self.start)

        self.register_plugin('xep_0066')
        self.register_plugin('xep_0071')
        self.register_plugin('xep_0128')
        self.register_plugin('xep_0363')

    def send_img(self, img):
        """send an img to the correspondant

        :img: PIL Image

        """
        img.save(self._IMG_FILE_PATH)
        self.connect()
        thread = threading.Thread(
                target=self.loop.run_until_complete,
                args=(self.disconnected, ),
                daemon=True,
                )
        thread.start()
        return thread

    def terminate(self):
        """will cancel all tasks for proper shutdown
        :returns: TODO

        """
        pending = asyncio.all_tasks(loop=self.loop)
        for task in pending:
            task.cancel()

    async def start(self, event):
        logging.info('Uploading image...')
        upload_file = self['xep_0363'].upload_file
        try:
            url = await upload_file(
                    self._IMG_FILE_PATH,
                    timeout=10,
            )
        except IqTimeout:
            self.disconnect()
            raise TimeoutError('Could not send message in time')
        logging.info('Upload success!')

        logging.info('Sending image to %s', self._correspondant)
        html = (
            f'<body xmlns="http://www.w3.org/1999/xhtml">'
            f'<a href="{url}">{url}</a></body>'
        )
        message = self.make_message(
                mto=self._correspondant,
                mbody=url,
                mhtml=html,
                )
        message['oob']['url'] = url
        message.send()
        logging.info('msg sent')
        self.disconnect()


class RegisterBot(slixmpp.ClientXMPP):

    """
    A basic bot that will attempt to register an account
    with an XMPP server.

    NOTE: This follows the very basic registration workflow
          from XEP-0077. More advanced server registration
          workflows will need to check for data forms, etc.
    """

    def __init__(self, jabber_id, password):

        self._jabber_id = jabber_id
        slixmpp.ClientXMPP.__init__(self, jabber_id, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The register event provides an Iq result stanza with
        # a registration form from the server. This may include
        # the basic registration fields, a data form, an
        # out-of-band URL, or any combination. For more advanced
        # cases, you will need to examine the fields provided
        # and respond accordingly. Slixmpp provides plugins
        # for data forms and OOB links that will make that easier.
        self.add_event_handler("register", self.register)

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data forms
        self.register_plugin('xep_0066')  # Out-of-band Data
        self.register_plugin('xep_0077')  # In-band Registration
        self['xep_0077'].force_registration = True

    async def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        await self.get_roster()

        # We're only concerned about registering, so nothing more to do here.
        self.disconnect()

    async def register(self, iq):
        """
        Fill out and submit a registration form.

        The form may be composed of basic registration fields, a data form,
        an out-of-band link, or any combination thereof. Data forms and OOB
        links can be checked for as so:

        if iq.match('iq/register/form'):
            # do stuff with data form
            # iq['register']['form']['fields']
        if iq.match('iq/register/oob'):
            # do stuff with OOB URL
            # iq['register']['oob']['url']

        To get the list of basic registration fields, you can use:
            iq['register']['fields']
        """
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
            path = os.path.join(DATA_DIR_PATH, ACCOUNTS_CREATED_FILE)
            config = configparser.ConfigParser()
            config[self._jabber_id] = {}
            with open(path, 'w') as configfile:
                config.write(configfile)
            self.disconnect()
        except IqError as e:
            logging.error(
                    "Could not register account: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()


class CredentialsHandlerError(Exception):
    pass


class CredentialsHandler(object):

    """a help to create, save and reload credentials for jabber account"""

    _DOMAIN = '@jabber.fr'
    _CRED_FILE = 'cred.ini'
    _KEY_FILE = '.key'

    def __init__(self):
        pass

    def create_and_save_new_cred(self, force=False):
        """will create new credentials. uses the user name,
        host and current day

        """
        credentials, key = self._create_new_cred()
        self._save_key(key, force)
        self._save_credentials(credentials, force)
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
        encrypted_pass = f.encrypt(password.encode()).decode()
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

    def _save_key(self, key, force):
        path = os.path.join(DATA_DIR_PATH, self._KEY_FILE)
        if os.path.exists(path) and not force:
            msg = 'a key file already existsü'
            raise CredentialsHandlerError(msg)
        with open(path, 'wb') as keyfile:
            pickle.dump(key.decode(), keyfile)

    def _load_key(self):
        path = os.path.join(DATA_DIR_PATH, self._KEY_FILE)
        with open(path, 'rb') as keyfile:
            key = pickle.load(keyfile).encode()
        return key

    def _save_credentials(self, credentials, force):
        path = os.path.join(DATA_DIR_PATH, self._CRED_FILE)
        if os.path.exists(path) and not force:
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
    pass
