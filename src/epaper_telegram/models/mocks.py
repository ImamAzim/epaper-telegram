from PIL import Image


class EPD2in13Mock():

    def display(self, img):
        """

        :img: TODO
        :returns: TODO

        """
        img.show()

class GT1151Mock():

    def input(self):
        x_str = input('x=')
        y_str = input('y=')
        return int(x_str), int(y_str)

    def wait_for_gesture(self):
        input('press enter to sim a gesture:\n')

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        pass
