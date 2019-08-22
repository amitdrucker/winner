from datetime import datetime

# 2 hours
BATCH_TIME_FRAME_SECONDS = 60 * 60 * 2
MIN_GAIN = 0.1
EVENTS_BACK = 20


def to_date_obj(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')


def mean(a, b):
    return (a + b) / 2
