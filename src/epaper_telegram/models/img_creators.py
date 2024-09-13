import time
from threading import Thread, Event
from queue import Queue, Empty
import logging


from PIL import Image, ImageDraw


class DrawToolError(Exception): pass


class DrawTool(object):

    """this class will take coordinates, draw them and send it to a displayer.
    it includes a menu for the user, so that it can ask for more coordinates
    or not"""
    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122
    _MENU_WIDTH = 60
    _DRAW_AREA = (_MENU_WIDTH, 0, _IMG_WIDTH, _IMG_HEIGHT)
    _SEND_AREA = (0, 0, _MENU_WIDTH, _IMG_HEIGHT / 3)
    _ERASE_AREA = (0, _IMG_HEIGHT / 3, _MENU_WIDTH, _IMG_HEIGHT * 2 / 3)
    _CANCEL_AREA = (0,  _IMG_HEIGHT / 3 * 2,_MENU_WIDTH, _IMG_HEIGHT * 3 / 3)

    def __init__(self, displayer):
        """
        :displayer: Displayer objet that uses the epd
        """
        self._displayer = displayer
        self._img = None

        self._queue = Queue()
        self._thread = Thread(target=self._process_coordinates_loop)
        self._running = Event()
        self._running.set()

    def point_to(self, x, y, s):
        """
        points the pen to coordinate x, y. If it is in the drawing area, it
        will be drawn on the image.
        When the displayer is ready, will update and the img with all
        the points will be sent to the displayer.
        if the point is on a menu, it can clear the image, or ask to stop
        (and ev return the img)

        :x: x coordinates to point on the display
        :y: y coordinates to point on the display
        :returns: continue (boolean) and img (None or array)

        """
        self._check_started()
        self._queue.put((x, y, s))

    def clear_img(self):
        """will create a fresh img (with menu) and send it to the displayer

        """
        self._reset_img()
        self._send_image_to_displayer()

    def _send_image_to_displayer(self, sleep_after=False):
        img_for_displayer = self._img.copy()
        self._displayer.display_img(img_for_displayer, sleep_after=sleep_after)

    def _check_started(self):
        if self._thread.is_alive() is not True:
            msg = (
                    'thread has not started or has been terminated.',
                    'use start method or context manager',
                    )
            logging.exception(msg)
            raise DrawToolError(msg)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if self._thread.is_alive():
            self.terminate()

    def start(self):
        """start thread that will take handles coordinates input to display

        """
        if self._thread.is_alive():
            msg = 'thread has already started'
            logging.exception(msg)
            raise DisplayerError(msg)
        self.clear_img()
        self._thread.start()

    def terminate(self):
        """terminate the thread

        """
        self._check_started()
        self._running.clear()
        self._queue.put(None)

    def _reset_img(self):
        img = Image.new('L', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        draw = ImageDraw.Draw(img)
        draw.rectangle(self._DRAW_AREA, fill=255, outline=0)
        draw.rectangle(self._SEND_AREA, fill=255, outline=0)
        draw.rectangle(self._ERASE_AREA, fill=255, outline=0)
        draw.rectangle(self._CANCEL_AREA, fill=255, outline=0)
        self._img = img

    def _draw_point_on_img(self, x, y, s):
        length = s ** 0.5
        dx = length / 2
        draw = ImageDraw.Draw(self._img)
        draw.rectangle((x - dx, y - dx, x + dx, y + dx), fill=0)

    def _process_coordinates_loop(self):
        while self._running.is_set():
            self._displayer.wait_for_ready()
            coordinates = self._queue.get()
            if coordinates is not None:
                self._draw_point_on_img(*coordinates)
                for i in range(self._queue.qsize()):
                    try:
                        coordinates = self._queue.get(block=False)
                    except Empty:
                        logging.warning('queue of coordinates was empty, size test failed')
                    else:
                        if coordinates is not None:
                            self._draw_point_on_img(*coordinates)
                self._send_image_to_displayer()
        logging.info('terminates drawtool thread')
