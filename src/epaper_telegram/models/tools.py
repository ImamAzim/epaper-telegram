import os


from epaper_telegram import DAEMON_ENTRY_POINT


VENV_DIR = os.environ.get('VIRTUAL_ENV', '')
SCRIPT_DIR = os.path.join(VENV_DIR, 'bin')


class ConfiguratorError(Exception):
    pass


class Configurator(object):

    """class to configure the epaper-telegram daemon"""

    def __init__(self):
        pass

    def add_deamon_in_crontab(self):
        """to enable the app

        """
        exec_path = os.path.join(SCRIPT_DIR, DAEMON_ENTRY_POINT)
        if not os.path.exists(exec_path):
            msg = 'there is no script to run the daemon app'
            raise ConfiguratorError(msg)
        else:
            print('TODO: add crontab job')

    def remove_daemon_from_crontab(self):
        """to deactivate the app
        :returns: TODO

        """
        pass
