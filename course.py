course_times = ["8:00", "8:50", "9:50", "10:40", "11:30", "14:05", "14:55", "15:45", "16:40", "17:30", "18:30", "19:20",
                "20:10"]
areas = ["文理学部", "工学部", "信息学部", "医学部"]


class Course:
    def __init__(self):
        self.__name = ""  # 课程名字
        self.__rawPlace = ""  # 原生的尚未解析的地点数据，如： 3区，1-505
        self.__rawTime = ""  # 原生的尚未解析的时间数据，如：11-18周6-9节
        self.__day = 0  # 课程所在星期几,0代表星期一，6代表星期日

        self.__period = ""  # 课程的开始周和结束周
        self.__place = ""  # 课程地点
        self.__startWeek = 0  # 课程开始周
        self.__endWeek = 0  # 课程结束周
        # self.__duration = ""  # 课程时长
        self.__startTime = 0  # 课程开始时间
        self.__endTime = 0  # 课程结束时间
        self.__teacher = ""  # 任课老师姓名

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, value):
        self.__day = value

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, value):
        self.__period = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        self.__place = value

    # 课程时长
    @property
    def duration(self):
        return self.__endTime - self.__startTime

    @property
    def startWeek(self):
        return self.__startWeek

    @startWeek.setter
    def startWeek(self, value):
        self.__startWeek = value

    @property
    def endWeek(self):
        return self.__endWeek

    @endWeek.setter
    def endWeek(self, value):
        self.__endWeek = value

    @property
    def startTime(self):
        return self.__startTime

    @startTime.setter
    def startTime(self, value):
        self.__startTime = value

    @property
    def endTime(self):
        return self.__endTime

    @endTime.setter
    def endTime(self, value):
        self.__endTime = value

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, value):
        self.__teacher = value

    @property
    def rawPlace(self):
        return self.__rawPlace

    @rawPlace.setter
    def rawPlace(self, value):
        data = value.split("，")

        if data[1].strip().startswith("计"):
            self.__place = "计算机学院大楼" + data[1].strip().lstrip("计")
        else:
            area_num = int(data[0].strip().rstrip("区"))
            self.__place = areas[area_num - 1] + " " + data[1]
        self.__rawPlace = value

    @property
    def rawTime(self):
        return self.__rawTime

    @rawTime.setter
    def rawTime(self, value):
        data = value.split("周")
        # 设置开始周和结束周
        [self.__startWeek, self.__endWeek] = map(int, data[0].split("-"))
        # 设置开始节和结束节
        [self.__startTime, self.__endTime] = map(int, data[1].rstrip("节").split("-"))

        self.__rawTime = value

    def __str__(self):
        result = "name: " + self.__name + "\n"
        result += "place: " + self.place + "\n"
        result += "week: " + str(self.startWeek) + "-" + str(self.endWeek) + "\n"
        result += "time: " + str(self.startTime) + "-" + str(self.endTime) + "\n"
        result += "teacher: " + self.__teacher
        return result


from util import get_now_day, get_now_week, get_tomorrow_week, get_tomorrow_day, get_now


def get_schedule(courses, week, day):
    schedule = []
    for item in courses[day]:
        if item.startWeek <= week and item.endWeek >= week:
            schedule.append(item)
    return schedule


def get_today_schedule(courses):
    return get_schedule(courses, get_now_week(), get_now_day())


def get_tomorrow_schedule(courses):
    return get_schedule(courses, get_tomorrow_week(), get_tomorrow_day())


# 使用crontab 每天 8点 ，1点，5点半提醒上课

def get_recent_lesson(courses):
    schedule = get_today_schedule(courses)

    hour = get_now().hour

    up = (18 if hour < 16 else 21) if hour > 12 else 12
    for item in schedule:
        lessonHour = int(course_times[item.startTime].split(":")[0])
        print(lessonHour)
        if lessonHour >= hour and lessonHour < up:
            return item
    return None
