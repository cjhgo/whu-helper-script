from course import get_today_schedule, get_tomorrow_schedule, get_recent_lesson
from getTimeTable import getTimeTable
from login import getCookie
from config import config
from accouts import accouts
from mail import send_schedule, send_lesson

# 使用crontab 每天 8点 ，1点，5点半提醒上课
from util import log

logger = log()

for user in accouts:
    cookie = getCookie(user["username"], user["password"])
    if cookie is None:
        logger.error("user " + user["username"] + " login fail, maybe the password is wrong")
    else:
        lesson = get_recent_lesson(getTimeTable(cookie))
        if lesson is None:
            logger.info("user " + user["username"] + "recent lesson is None")
        else:
            send_lesson(user['email'], lesson)
