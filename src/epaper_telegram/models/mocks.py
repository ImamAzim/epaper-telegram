import logging


from PIL import Image


class EPD2in13Mock():

    def __init__(self):
        logging.info('open connections of edp')

    def display(self, img):
        """

        :img: TODO
        :returns: TODO

        """
        img.show()

    def __enter__(self):
        logging.info('reset epd')
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        logging.info('close connection of epd and deep sleep')

    def sleep(self):
        logging.info('sleep')

    def deep_sleep(self):
        logging.info('deep_sleep')

class GT1151Mock():

    def input(self):
        x_str = input('x=')
        y_str = input('y=')
        s_str = input('s=')
        return int(x_str), int(y_str), int(s_str)

    def wait_for_gesture(self):
        input('press enter to sim a gesture:\n')

    def __enter__(self):
        logging.info('reset GT')
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        logging.info('close connection of GT and sleep')
        pass
