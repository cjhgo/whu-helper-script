from email.mime.text import MIMEText
import smtplib
from __config import mail
from util import get_today, get_now_day, get_tomorrow, get_tomorrow_day, get_now_week
from course import course_times

week_day_zh = ["一", "二", "三", "四", "五", "六", "日"]


def sendMail(to_addr, subject, textBody, format="html", from_name="武大助手"):
    msg = MIMEText(textBody, format, 'utf-8')
    msg["Subject"] = subject
    msg["From"] = from_name
    msg["To"] = to_addr

    print(mail['smtp_server'])
    server = smtplib.SMTP_SSL(mail["smtp_server"], mail['ssl_port'])

    server.login(mail['addr'], mail['auth_code'])
    server.sendmail(mail['addr'], to_addr, msg.as_string())
    server.close()


def format_schedule(schedule):
    tomorrow = get_tomorrow()
    tomorrow_day = get_tomorrow_day()
    content = "明天是星期" + week_day_zh[tomorrow_day] + "," + str(tomorrow.year) + "年" + str(tomorrow.month) + "月" + str(
        tomorrow.day) + "日"
    content += "<br>"
    if len(schedule) > 0:
        content += "共有<b>" + str(len(schedule)) + "</b>节课"
        content += "<hr>"
        for lesson in schedule:
            if lesson.startTime < 6:
                # 上午的课
                content += "上午"
            elif lesson.startTime < 11:
                content += "下午"
            else:
                content += "晚上"

            content += course_times[lesson.startTime - 1] + "<br>"
            content += "课程名称： <b>" + lesson.name + "</b><br>"
            if len(lesson.place) > 0:
                content += "课程地点：<b>" + lesson.place + "</b><br>"
            if len(lesson.teacher) > 0:
                content += "教师：" + lesson.teacher + "<br>"
        content += "<br><hr>"
        content += "本周是第" + str(get_now_week()) + "周,"
        content += "新的一天，好好加油！"
    else:
        content += "明天没课，好好休息下哈~"

    return content


def format_lesson(lesson):
    content = ""
    content += course_times[lesson.startTime - 1] + "<br>"
    content += "课程名称： <b>" + lesson.name + "</b><br>"
    if len(lesson.place) > 0:
        content += "课程地点：<b>" + lesson.place + "</b><br>"
    if len(lesson.teacher) > 0:
        content += "教师：" + lesson.teacher + "<br>"
    content += "本周是第" + str(get_now_week()) + "周"
    return content


def send_schedule(mail, schedule):
    subject = "星期" + week_day_zh[get_tomorrow_day()] + "的课"
    sendMail(mail, subject, format_schedule(schedule))


def send_lesson(mail, lesson):
    subject = ""
    if lesson.startTime < 6:
        subject += "上午"
    elif lesson.startTime < 11:
        subject += "下午"
    else:
        subject += "晚上"
    subject += "上课提醒~"
    sendMail(mail, subject, format_lesson(lesson))


if __name__ == "__main__":
    pass
