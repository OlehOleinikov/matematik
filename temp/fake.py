import time


def fake_func():
    global counter_bs
    while counter_bs <100:
        time.sleep(1)
        counter_bs += 1