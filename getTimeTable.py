import requests
from bs4 import BeautifulSoup
from login import getCookie
from util import write_file
import re
from course import Course


def innerHTML(element):
    return element.decode_contents(formatter="html")


def getTimeTable(cookies):
    timetable_url = "http://yjs.whu.edu.cn/ssfw/pygl/xkgl/xskb.do"
    timeTable_data = requests.get(timetable_url, cookies=cookies)
    # write_file(timeTable_data.content, "timetable")
    return parser_timeTable(timeTable_data.content)


def parser_timeTable(html):
    soup = BeautifulSoup(html, "lxml")
    schedule = soup.select("tr.t_con")
    result = [[] for n in range(7)]
    last = [0 for n in range(7)]
    for row in schedule:
        courseInrow = row.select("td")
        isBegin = False  # 这节课有没有遍历到课程信息处
        index = 0
        for lesson in courseInrow:
            rawText = innerHTML(lesson)

            if isBegin == False and "第" in rawText and "节" in rawText:
                isBegin = True
                index = 0
            elif isBegin == True:
                while last[index] > 0 and index < 7:
                    last[index] -= 1
                    index += 1
                if index == 7:
                    break

                rawText = rawText.strip().strip("&nbsp;")

                if len(rawText) > 0:
                    last[index] += int(lesson['rowspan']) - 1
                    result[index].extend(parser_Course(rawText, index))
                index += 1
    return result


def parser_Course(rawContent, day):
    courses = []
    rawContent = rawContent.rstrip().rstrip("<br/>")
    # print(rawContent)
    courseList = rawContent.split("<br/>")  # 可能有多节课
    for rawCourse in courseList:
        courses.append(parser_Slice(rawCourse, day))
    return courses


def parser_Slice(rawCourse, day):
    slices = re.split("\\s|\\n", rawCourse.strip())
    course = Course()
    course.day = day  # 设置星期几
    for index, item in enumerate(slices):
        item = item.strip()
        if index == 0:
            course.name = item  # 第一个肯定是课程名字
        elif "周" in item and "节" in item:
            # 时间
            course.rawTime = item
        elif "区" in item and item[0].isnumeric():
            # 地点
            course.rawPlace = item
            pass
        else:
            course.teacher = item
    return course


if __name__ == "__main__":
    # course = "分布并行计算机技术16硕 11-18周6-9节 3区，1-505  黄传河<br>高级操作系统16硕 2-10周6-9节 1区，计-201  何炎祥<br>"
    # data = parser_Course(course)
    # for index, item in enumerate(data):
    #     print("第" + str(index + 1) + "节课")
    #     print(item)

    data = getTimeTable(getCookie())
    for index, day in enumerate(data):
        print("星期" + str(index + 1))
        print("共有" + str(len(day)) + "节课")
        if len(day) == 0:
            print("课程为空")
            continue
        for lesson in day:
            if lesson == None:
                print(None)
            else:
                print(lesson)
