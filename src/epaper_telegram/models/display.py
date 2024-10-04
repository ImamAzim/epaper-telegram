from threading import RLock, Thread, Event
import queue
import logging


from waveshare_touch_epaper import epaper_models
from waveshare_touch_epaper.epaper_display import BaseEpaper, EpaperException


class DisplayerError(Exception):
    pass


class Displayer(object):

    """object that will take img array and display on epaper (epd waveshare).
    Should be the only one to use this resource"""
    _MENU_WIDTH = 60

    def __init__(self, epaper_model_name: str):
        """
        :mock_mode: boolean. use a mock epd display if True
        """
        self._rlock = RLock()
        self._queue = queue.Queue(maxsize=1)
        self._thread = Thread(target=self._process_img_loop, daemon=None)
        self._running = Event()
        self._running.set()

        self._EPD = epaper_models[epaper_model_name]

    @property
    def WIDTH(self):
        return self._EPD.WIDTH

    @property
    def HEIGHT(self):
        return self._EPD.HEIGHT

    @property
    def MENU_WIDTH(self):
        return self._MENU_WIDTH

    def _check_started(self):
        if self._thread.is_alive() is not True:
            msg = (
                    'thread has not started or has been terminated.',
                    'use start method or context manager',
                    )
            logging.exception(msg)
            raise DisplayerError(msg)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self._thread.is_alive():
            self.terminate()

    def start(self):
        """start thread that will allow to display img.

        """
        if self._thread.is_alive():
            msg = 'thread has already started'
            logging.exception(msg)
            raise DisplayerError(msg)
        self._thread.start()

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
        (img=None will be accepted and is used internally to terminate)
        :sleep_after: bool, put the display to sleep after task done
        :block: bool, same function as in a queue object
        :timeout: bool or positive number, same function as in a queue object

        """
        self._check_started()
        self._queue.put((img, sleep_after), block=block, timeout=timeout)

    def wait_for_ready(self):
        """block until the displayer has finished his job and is ready to
        accept an img.

        """
        self._check_started()
        self._queue.join()

    def terminate(self):
        """terminate the thread and put the epd to sleep

        """
        self._check_started()
        self._running.clear()
        try:
            self.display_img(None, timeout=1)
        except queue.Full:
            logging.debug('process_img_loop has probably exited the loop')
            self._queue.task_done()

    def _process_img_loop(self):
        while self._running.is_set():
            img, sleep_after = self._queue.get()
            if img is None:
                self._queue.task_done()
            else:
                epd: BaseEpaper
                with self._EPD() as epd:
                    epd.display(img, full=True, wait=False)
                    self._queue.task_done()
                    while not sleep_after:
                        img, sleep_after = self._queue.get()
                        if img is not None:
                            try:
                                epd.display(img, full=False, wait=False)
                            except EpaperException:
                                epd.display(img, full=True, wait=False)
                        self._queue.task_done()
