
class ConfigureMenu(object):

    """view in shell with a menu to configure epaper-telegram"""

    def __init__(self):
        self._menu = {
                '1': 'set correspondant',
                '2': 'activate epaper-telegram',
                '3': 'de-activate epaper-telegram',
                'q': 'quit',
                }
        self._running = True

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

    def _print_welcome(self):
        print(
                'welcome to epaper-telegram configurator menu'
                )
        print('===')

    def _print_menu(self):

        print(f'your jabber id: {self._user_jid}')
        print(f'correspondant jabber id: {self._corresp_jid}')

        for key, value in self._menu.items():
            print(key, value)
        print('===')

    def case_1(self):
        """set correspondant

        """

    def case_2(self):
        """activate epaper in crontab

        """
        print('===')

    def case_3(self):
        """deactivate epaper in crontab

        """
        print('===')

    def case_q(self):
        """quit

        """
        print('goodbye')
        self._running = False
