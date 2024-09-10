from threading import RLock
import queue


class Displayer(object):

    """object that will take img array and display on epaper (epd waveshare).
    Should be the only one to use this resource"""

    def __init__(self):
        self._rlock = RLock()
        self._queue = queue.Queue(maxsize=1)

    @property
    def rlock(self):
        """a re-entrant lock than can be used to prevent other threads
        to use the displayer at the same time
        :returns: rlock

        """
        return self._rlock

    def display_img(self, img, sleep_after=True, block=True, timeout=None):
        """the img will we put in a queue and display once the worker is ready.
        to avoid being blocked, one can use the wait_for_ready method
        there is only one slot available in the queue.

        :img: array of dim (250, 122) to be displayed
        :sleep_after: bool, put the display to sleep after task done
        :block: bool, same function as in a queue object
        :timeout: bool or positive number, same function as in a queue object

        """
        pass

    def wait_for_ready(self):
        """block until the displayer has finished his job and is ready to
        accept an img.

        """
        pass
