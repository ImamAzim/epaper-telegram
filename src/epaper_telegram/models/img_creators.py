import time
from threading import Thread, Event
from queue import Queue, Empty
import logging
import os


from PIL import Image, ImageDraw


class DrawToolError(Exception): pass


class DrawTool(object):

    """this class will take coordinates, draw them and send it to a displayer.
    it includes a menu for the user, so that it can ask for more coordinates
    or not"""
    _PIC_FOLDER = os.path.join(
            os.path.dirname(__file__),
            '..',
            'pics'
            )
    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122
    _MENU_WIDTH = 60
    _DRAW_AREA_COORDINATES = (_MENU_WIDTH, 0, _IMG_WIDTH, _IMG_HEIGHT)
    _BUTTONS_AREAS = dict(
            send=dict(icon='send.jpg', row=0),
            erase=dict(icon='erase.bmp', row=1),
            cancel=dict(icon='cancel.jpg', row=2),
            )
    _BUTTON_HEIGHT = _IMG_HEIGHT / len(_BUTTONS_AREAS)
    for key, el in _BUTTONS_AREAS.items():
        el['coordinates'] = (
                0,
                _BUTTON_HEIGHT * el['row'],
                _MENU_WIDTH,
                _BUTTON_HEIGHT * (el['row'] + 1),
                )

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

        (x1, y1, x2, y2) = self._DRAW_AREA_COORDINATES
        if x >= x1 and x <= x2 and y >= y1 and y <= y2:
            self._queue.put((x, y, s))
            return True, None
        for key, el in self._BUTTONS_AREAS.items():
            coordinates = el['coordinates']
            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                to_continue, img = getattr(self, f'_{key}_button')()
                return to_continue, img


    def _send_button(self):
        pass

    def _cancel_button(self):
        pass

    def _erase_button(self):
        pass

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
        img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        draw = ImageDraw.Draw(img)
        draw.rectangle(self._DRAW_AREA_COORDINATES, fill=255, outline=0)
        i = 0
        for button_name, button_dict in self._BUTTONS_AREAS.items():
            draw.rectangle(button_dict['coordinates'], fill=255, outline=0)
            max_size = self._MENU_WIDTH, self._BUTTON_HEIGHT
            path = os.path.join(self._PIC_FOLDER, button_dict['icon'])
            button_img = Image.open(path)
            button_img.thumbnail(max_size)
            w, h = button_img.size
            center = self._MENU_WIDTH / 2, self._BUTTON_HEIGHT * (i + 1 / 2)
            top_left_corner = int(center[0]- w / 2), int(center[1] - h / 2)
            img.paste(button_img, top_left_corner)
            i += 1
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
