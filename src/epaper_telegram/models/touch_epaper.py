import threading
import logging


from waveshare_touch_epaper import gt1151, epd2in13_V4


class EpdTouch2In13(object):

    """handle waveshare touch epaper display 2inch13.
    both display and touch device"""

    def __init__(self):

        self._flag_t = 1

        self._epd = epd2in13_V4.EPD()
        self._gt = gt1151.GT1151()
        self._GT_Dev = gt1151.GT_Development()
        self._GT_Old = gt1151.GT_Development()

        logging.info("init touch screen")

        self._gt.GT_Init()
        self._thread_gt = threading.Thread(target=self._pthread_irq)
        self._thread_gt.setDaemon(True)

    def _pthread_irq(self):
        logging.info("pthread running")
        while self._flag_t == 1:
            if self._gt.digital_read(self._gt.INT) == 0:
                self._GT_Dev.Touch = 1
            else:
                self._GT_Dev.Touch = 0
        logging.info("thread:exit")

    def turn_on(self):
        """switch on device
        :returns: TODO

        """
        self._thread_gt.start()
        self._epd.init(self._epd.FULL_UPDATE)
        self._gt.GT_Init()
        self._epd.Clear(0xFF)

        self._epd.init(self._epd.PART_UPDATE)

    def turn_off(self):
        """sleep mode and close all port
        :returns: TODO

        """
        flag_t = 0
        self._epd.sleep()
        time.sleep(2)
        self._thread_gtt.join()
        self._epd.Dev_exit()
