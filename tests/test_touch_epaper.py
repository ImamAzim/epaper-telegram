import time


from epaper_telegram.models.touch_epaper import GT1151


def touch_screen():
    print('normal test...')
    gt = GT1151()
    gt.start()
    time.sleep(2)
    gt.stop()

    print('test with context manager')
    with GT1151() as gt:
        print('touch has started')
        time.sleep(2)
    print('touch should be closed')


if __name__ == '__main__':
    touch_screen()
