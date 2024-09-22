from threading import Thread, Event, Timer
from queue import Queue, Empty
import logging
import os


from PIL import Image, ImageDraw


from epaper_telegram.models.display import DisplayerError
from epaper_telegram.models.xmpp import ImageTransferBotError


class DrawToolError(Exception):
    pass


class OnlineImageDownloaderError(Exception):
    pass


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
                int(_BUTTON_HEIGHT * el['row']),
                int(_MENU_WIDTH),
                int(_BUTTON_HEIGHT * (el['row'] + 1)),
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
            (x1, y1, x2, y2) = el['coordinates']
            if x >= x1 and x <= x2 and y >= y1 and y <= y2:
                to_continue, img = getattr(self, f'_{key}_button')()
                return to_continue, img
        logging.warning('coordinates are not in any expected area')
        return True, None

    def _send_button(self):
        to_continue = False
        img = self._img.copy()
        return to_continue, img

    def _cancel_button(self):
        to_continue = False
        img = None
        return to_continue, img

    def _erase_button(self):
        to_continue = True
        img = None
        self.clear_img()
        return to_continue, img

    def clear_img(self):
        """will create a fresh img (with menu) and send it to the displayer

        """
        self._reset_img()
        self._send_image_to_displayer()

    def _send_image_to_displayer(self, sleep_after=False):
        img_for_displayer = self._img.copy()
        try:
            self._displayer.display_img(
                    img_for_displayer,
                    sleep_after=sleep_after,
                    )
        except DisplayerError:
            logging.warning('did not success to display img')

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
            raise DrawToolError(msg)
        self._displayer.rlock.acquire()
        self.clear_img()
        self._thread.start()

    def terminate(self):
        """terminate the thread

        """
        self._check_started()
        self._running.clear()
        self._queue.put(None)
        self._displayer.rlock.release()

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
            top_left_corner = int(center[0] - w / 2), int(center[1] - h / 2)
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
                        msg = (
                                'queue of coordinates was empty',
                                ', size test failed')
                        logging.warning(msg)
                    else:
                        if coordinates is not None:
                            self._draw_point_on_img(*coordinates)
                self._send_image_to_displayer()
        logging.info('terminates drawtool thread')


class OnlineImageDownloader(object):

    """this class will run a thread continuously and regulary check online
    if a new image is available. when it is, it will send it to the display"""

    _MENU_WIDTH = 60
    _MENU_HEIGHT = 122
    _IMG_WIDTH = 250
    _IMG_HEIGHT = 122

    def __init__(self, displayer, img_transfer_bot):
        """
        :displayer: Displayer objet that uses the epd
        :online_img_tool: OnlineImg object to upload and download img
        """
        self._displayer = displayer
        self._img = Image.new('1', (self._IMG_WIDTH, self._IMG_HEIGHT), 255)
        self._img_transfer_bot = img_transfer_bot

        self._thread = Thread(target=self._check_online_img)
        self._running = Event()
        self._running.set()

    def _check_started(self):
        if self._thread.is_alive() is not True:
            msg = (
                    'thread has not started or has been terminated.',
                    'use start method or context manager',
                    )
            logging.exception(msg)
            raise OnlineImageDownloaderError(msg)

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
            raise OnlineImageDownloaderError(msg)
        self._thread.start()

    def terminate(self):
        """terminate the thread

        """
        self._check_started()
        self._running.clear()
        self._img_transfer_bot.stop_waiting()

    def display_now(self):
        """a method to use if the display was cleared and we want to redisplay
        the online img even if it has not been changed

        """
        img = self._adapt_img()
        with self._displayer.rlock:
            try:
                self._displayer.display_img(
                        img,
                        sleep_after=True,
                        )
            except DisplayerError:
                logging.exception('did not success to display img')

    def upload(self, img):
        """upload img online

        :img: Image PIL object

        """
        self._img_transfer_bot.send_img(img)

    def _adapt_img(self):
        img = self._img.copy()
        draw = ImageDraw.Draw(img)
        draw.rectangle(
                (0, 0, self._MENU_WIDTH, self._MENU_HEIGHT),
                outline=0,
                fill=255,
                )
        start = self._MENU_WIDTH / 2, 0.9 * self._MENU_HEIGHT
        end = self._MENU_WIDTH / 2, 0.1 * self._MENU_HEIGHT
        draw.line((start, end))
        x1 = end
        x2 = end[0] - 5, end[1] + 5
        x3 = end[0] + 5, end[1] + 5
        draw.polygon((x1, x2, x3), fill=0)
        return img

    def _get_latest_img(self):
        try:
            online_img = self._img_transfer_bot.img
        except ImageTransferBotError:
            msg = 'could not get a received img'
            logging.exception(msg)
        else:
            self._img = online_img

    def _check_online_img(self):
        while self._running.is_set():
            self._get_latest_img()
            self.display_now()
            self._img_transfer_bot.wait_for_msg()

        logging.info('terminates online image downloader thread')


if __name__ == '__main__':
    timer = Timer(10, lambda: print('ok'))
    timer.cancel()
