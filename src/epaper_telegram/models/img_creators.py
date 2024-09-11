from threading import Thread
from queue import Queue


from PIL import Image


class DrawTool(object):

    """this class will take coordinates, draw them and send it to a displayer.
    it includes a menu for the user, so that it can ask for more coordinates or not"""

    def __init__(self, displayer):
        """TODO: to be defined.
        :displayer: Displayer objet that uses the epd
        """
        self._displayer = displayer
        self._img = None

        self._queue = queue.Queue()
        self._thread = Thread(target=self._process_coordinates_loop, daemon=True)
        self._thread.start()

        self._reset_img()


    def point_to(self, x, y):
        """
        points the pen to coordinate x, y. If it is in the drawing area, it will be drawn on the image.
        When the displayer is ready, will update and the img with all
        the points will be sent to the displayer.
        if the point is on a menu, it can clear the image, or ask to stop (and ev return the img)

        :x: x coordinates to point on the display
        :y: y coordinates to point on the display
        :returns: continue (boolean) and img (None or array)

        """
        pass

    def clear_img(self):
        """will create a fresh img (with menu) and send it to the displayer
        :returns: TODO

        """
        pass

    def _reset_img(self):
        pass

    def _process_coordinates_loop(self):
        while True:
            pass
