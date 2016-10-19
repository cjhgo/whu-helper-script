import requests
from bs4 import BeautifulSoup
from util import write_file, log

logger = log()


def getCookie(username, password):
    login_url = "http://cas.whu.edu.cn/authserver/login?service=http://my.whu.edu.cn"

    s = requests.Session()
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
    }
    s.headers.update(headers)

    login_data = s.get(login_url)
    params = parse_param(login_data.content, username, password)
    r = s.post(login_url, data=params)
    if "欢迎访问武汉大学校园信息门户" in r.text:
        logger.info("login success")
        return s.cookies
    return None


# 获取令牌及数据
def parse_param(html, username, password):
    soup = BeautifulSoup(html, "lxml")
    params = {"username": username,
              "password": password}

    input_hidden = soup.select("#casLoginForm input[type=hidden]")

    for item in input_hidden:
        params[item['name']] = item['value']
    return params


# 获取用户的真实名字
def get_name(cookie):
    main_url = "http://my.whu.edu.cn/"
    html = requests.get(main_url, cookies=cookie)
    soup = BeautifulSoup(html.content, "lxml")
    rawText = soup.select("div.composer li")[0].get_text()
    name = rawText.split("var")[0].strip()
    return name


if __name__ == "__main__":
    pass
