class Displayer(object):

    """object that will take img array and display on epaper (epd waveshare).
    Should be the only one to use this resource"""

    def __init__(self):
        pass

    def display_img(self, img, block=True, timeout=None):
        """the img will we put in a queue and display once the worker is ready.
        to avoid being blocked, one can use the wait_for_ready method

        :img: array of dim (250, 122) to be displayed
        :block: bool, same function as in a queue object
        :timeout: bool or positive number, same function as in a queue object

        """
        pass
