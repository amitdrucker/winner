from datetime import datetime


def to_date_obj(date_str):
    return datetime.strptime(date_str, '%H:%M:%S')


def mean(a, b):
    return (a + b) / 2
