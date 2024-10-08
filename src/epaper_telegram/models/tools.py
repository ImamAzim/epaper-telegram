import getpass
import os
import sys


from crontab import CronTab


from epaper_telegram import DAEMON_ENTRY_POINT


class ConfiguratorError(Exception):
    pass


class Configurator(object):

    """class to configure the epaper-telegram daemon"""
    _CRONJOB_ID = 'epaper-telegram'

    def __init__(self):
        pass

    def add_deamon_in_crontab(self):
        """to enable the app

        """

        exec_path = os.path.join(sys.exec_prefix, 'bin', DAEMON_ENTRY_POINT)
        if not os.path.exists(exec_path):
            msg = 'there is no script to run the daemon app'
            print(msg)
            raise ConfiguratorError(msg)

        cron = CronTab(user=True)
        if [el for el in cron.find_comment(self._CRONJOB_ID)]:
            msg = 'epaper-telegram is already activated'
            print(msg)
            raise ConfiguratorError

        tmp_file = f'/tmp/epaper-telegram_log_{getpass.getuser()}'
        job = cron.new(
                command=f'{exec_path} -l > {tmp_file} 2>&1',
                comment=self._CRONJOB_ID,
                )
        job.every_reboot()

        cron.write()

    def remove_daemon_from_crontab(self):
        """to deactivate the app

        """
        cron = CronTab(user=True)
        cron.remove_all(comment=self._CRONJOB_ID)
        cron.write()
