import os
import sys


from epaper_telegram import DAEMON_ENTRY_POINT


class ConfiguratorError(Exception):
    pass


class Configurator(object):

    """class to configure the epaper-telegram daemon"""

    def __init__(self):
        pass

    def add_deamon_in_crontab(self):
        """to enable the app

        """

        executed_path = sys.argv[0]
        abso_executed_path = os.path.abspath(executed_path)
        bin_dir = os.path.dirname(abso_executed_path)
        exec_path = os.path.join(bin_dir, DAEMON_ENTRY_POINT)
        print(exec_path)
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
