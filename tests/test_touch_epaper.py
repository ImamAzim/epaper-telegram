import time


from epaper_telegram.models.touch_epaper import GT1151


def touch_screen():
    gt = GT1151()
    gt.start()
    time.sleep(2)
    gt.stop()


if __name__ == '__main__':
    touch_screen()
