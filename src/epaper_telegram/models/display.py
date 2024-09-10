from threading import RLock, Thread, Event
import queue


class Displayer(object):

    """object that will take img array and display on epaper (epd waveshare).
    Should be the only one to use this resource"""
    _TIMEOUT = 120

    def __init__(self):
        self._rlock = RLock()
        self._queue = queue.Queue(maxsize=1)
        self._thread = Thread(target=self._process_img_loop, daemon=None)
        self._running = Event()
        self._running.set()
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
        self._queue.put((img, sleep_after), block=block, timeout=timeout)

    def wait_for_ready(self):
        """block until the displayer has finished his job and is ready to
        accept an img.

        """
        self._queue.join()

    def terminate(self):
        """terminate the thread and put the epd to sleep

        """
        self._running.clear()
        self.display_img(None)

    def _process_img_loop(self):
        while self._running.is_set():
            try:
                img, sleep_after = self._queue.get(timeout=self._TIMEOUT)
            except queue.Empty:
                msg = 'no img received for a long time. go to sleep.'
                print(msg)
                print('TODO: got to sleep')
            else:
                if img is not None:
                    print('TODO: display img')
                    if sleep_after:
                        print('TODO: put display to sleep')
                self._queue.task_done()
        print('go to sleep because thread terminated')
