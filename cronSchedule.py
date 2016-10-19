from course import get_today_schedule, get_tomorrow_schedule
from getTimeTable import getTimeTable
from login import getCookie
from config import config
from accouts import accouts
from mail import send_schedule
from util import log

logger = log()

for user in accouts:
    cookie = getCookie(user["username"], user["password"])
    if cookie is None:
        logger.error("user " + user["username"] + "login fail, maybe the password is wrong")
    else:
        schedule = get_tomorrow_schedule(getTimeTable(cookie))
        send_schedule(user["email"], schedule)
