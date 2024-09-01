import threading
import logging


from gpiozero.pins.native import NativeFactory
from gpiozero import Device
Device.pin_factory = NativeFactory()
from waveshare_touch_epaper import gt1151, epd2in13_V4


class EpdTouch2In13(object):

    """handle waveshare touch epaper display 2inch13. both display and touch device"""

    def __init__(self):

        self._flag_t = 1

        self._epd = epd2in13_V4.EPD()
        self._gt = gt1151.GT1151()
        self._GT_Dev = gt1151.GT_Development()
        self._GT_Old = gt1151.GT_Development()

        logging.info("init touch screen")

        self._gt.GT_Init()
        self._thread_gt = threading.Thread(target = self._pthread_irq)
        self._thread_gt.setDaemon(True)

    def _pthread_irq() :
        print("pthread running")
        while self._flag_t == 1 :
            if(gt.digital_read(gt.INT) == 0) :
                GT_Dev.Touch = 1
            else :
                GT_Dev.Touch = 0
        print("thread:exit")
