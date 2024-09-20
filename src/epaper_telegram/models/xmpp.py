import datetime
import os
import getpass
import logging


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

    def __init__(self):
        pass

    def create_and_save_new_cred(self):
        """will create new credentials. uses the user name, host and current day

        """
        credentials = self._create_new_cred()


    def _create_new_cred(self):
        user = getpass.getuser()
        host = os.uname()[1]
        date = datetime.date.today()
        username = f'{user}_{host}_{date}_BOT'
        jabber_id = username + self._DOMAIN
        password = 'pass'
        credentials = dict(
                jabber_id=jabber_id,
                password=password,
                )
        return credentials


if __name__ == '__main__':
    credential_handler = CredentialsHandler()
    credentials = credential_handler._create_new_cred()
    print(credentials)
