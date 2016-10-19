import datetime
import math
import logging


def write_file(content, filename="temp"):
    with open(filename, "wb") as code:
        code.write(content)


# 获取今天是第几周,
# opening_date_str 形如2016-09-04
def get_now_week(opening_date_str="2016-09-04"):
    opening_date = datetime.datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    today = datetime.date.today()
    days = (today - opening_date).days + 1
    return math.ceil(days / 7)


def get_tomorrow_week(opening_date_str="2016-09-04"):
    opening_date = datetime.datetime.strptime(opening_date_str, '%Y-%m-%d').date()
    tomorrow = get_tomorrow()
    days = (tomorrow - opening_date).days + 1
    return math.ceil(days / 7)


# 获取今天是星期几，星期一是0，星期日是6
def get_now_day():
    return datetime.datetime.now().weekday()


def get_tomorrow_day():
    return get_tomorrow().weekday()


def get_today():
    return datetime.date.today()


def get_tomorrow():
    return get_today() + datetime.timedelta(days=1)


def get_now():
    return datetime.datetime.now()


def log():
    logging.basicConfig(level=logging.INFO)
    return logging


if __name__ == "__main__":
    log().debug('This is debug message')
