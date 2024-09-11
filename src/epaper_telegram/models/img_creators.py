class DrawTool(object):

    """this class will take coordinates, draw them and send it to a displayer.
    it includes a menu for the user, so that it can ask for more coordinates or not"""

    def __init__(self, displayer):
        """TODO: to be defined.
        :displayer: Displayer objet that uses the epd
        """
        self._displayer = displayer

    def point_to(self, x, y):
        """
        points the pen to coordinate x, y. If it is in the drawing area, it will be drawn on the image.
        When the displayer is ready, will update the img with all
        the points and send it to be displayed on the displayer queue.
        if the point is on a menu, it can clear the image, or ask to stop (and ev return the img)

        :x: x coordinates to point on the display
        :y: y coordinates to point on the display
        :returns: continue (boolean) and img (None or array)

        """
        pass
