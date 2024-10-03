from varboxes import VarBox


from waveshare_touch_epaper import touchscreen_models


from epaper_telegram.models.tools import Configurator, ConfiguratorError
from epaper_telegram import APP_NAME


class ConfigureMenu(object):

    """view in shell with a menu to configure epaper-telegram"""

    def __init__(self):
        self._menu = {
                '0': 'set touch screen model',
                '1': 'set correspondant',
                '2': 'activate epaper-telegram',
                '3': 'de-activate epaper-telegram',
                'q': 'quit',
                }
        self._running = True
        self._vb = VarBox(APP_NAME)
        try:
            self._corresp_jid = self._vb.corresp_jid
        except AttributeError:
            self._corresp_jid = 'None'

        self._configurator = Configurator()

    def start(self, user_jid):

        self._user_jid = user_jid

        self._print_welcome()
        while self._running:
            self._print_menu()
            choice = input('please select:\n')
            try:
                getattr(self, f'case_{choice}')()
            except AttributeError:
                print('please select a valid option')
            print('===================================================')

    def _print_welcome(self):
        print(
                'welcome to epaper-telegram configurator menu'
                )

    def _print_menu(self):
        print('===================================================')

        print(f'your jabber id: {self._user_jid}')
        print(f'correspondant jabber id: {self._corresp_jid}')

        for key, value in self._menu.items():
            print(key, value)
        print('===================================================')

    def case_0(self):
        """set touch screen model

        """
        options = {
                str(index): model for index, model
                in enumerate(touchscreen_models)}
        for index, model in options.items():
            print(f'{index}: {model}')
        index = input(f'chose yoour model (0-{len(options)-1}):\n')
        try:
            model = options[index]
        except KeyError:
            print('error in your choice')
        else:
            print(f'the model used will be {model}:')
            print(touchscreen_models[model].__doc__)
            self._vb.touch_model_name = model

    def case_1(self):
        """set correspondant

        """
        corresp_jid = input('enter the jabber id of your correspondant:\n')
        self._vb.corresp_jid = corresp_jid
        self._corresp_jid = corresp_jid

    def case_2(self):
        """activate epaper in crontab

        """
        try:
            self._configurator.add_deamon_in_crontab()
        except ConfiguratorError:
            pass
        print('===')

    def case_3(self):
        """deactivate epaper in crontab

        """
        try:
            self._configurator.remove_daemon_from_crontab()
        except ConfiguratorError:
            pass
        print('===')

    def case_q(self):
        """quit

        """
        print('goodbye')
        self._running = False
