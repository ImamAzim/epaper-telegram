import threading
import logging


from waveshare_touch_epaper import gt1151, epd2in13_V4


class Epd2In13Display(object):

    """display part of the 2.13 inch touch epaper display"""

    def __init__(self):
        self._epd = epd2in13_v4.epd()

        self._epd.init(self._epd.FULL_UPDATE)
        self._epd.Clear(0xFF)
        self._epd.init(self._epd.PART_UPDATE)

    def turn_off(self):
        """sleep mode and close all port
        :returns: TODO

        """
        self._epd.sleep()
        time.sleep(2)
        self._epd.Dev_exit()


class EGT1151(object):

    """touch screen part of the 2.13 inch touch epaper display"""

    def __init__(self):

        self._flag_t = 1

        self._gt = gt1151.gt1151()
        self._gt_dev = gt1151.gt_development()
        self._gt_old = gt1151.gt_development()

        logging.info("init touch screen")

        self._gt.gt_init()
        self._thread_gt = threading.Thread(target=self._pthread_irq)
        self._thread_gt.setDaemon(True)

        self._ready = False
        self._stopped = False

    def _pthread_irq(self):
        logging.info("pthread running")
        while self._flag_t == 1:
            if self._gt.digital_read(self._gt.INT) == 0:
                self._GT_Dev.Touch = 1
            else:
                self._GT_Dev.Touch = 0
        logging.info("thread:exit")

    def start(self):
        """start the thread and init the touch device
        :returns: TODO

        """
        if not self._stopped:
            self._thread_gt.start()
            self._gt.GT_Init()
            self._ready = True

    def stop(self):
        """close the port for the touch and finish thread
        :returns: TODO

        """

        if not self._stopped:
            flag_t = 0
            self._thread_gtt.join()
            self._stopped = True
