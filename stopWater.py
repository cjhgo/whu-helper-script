import codecs
import datetime

import requests
from __accouts import accouts
from bs4 import BeautifulSoup

from mail import sendMail
from util import get_today
from lastArticle import last_article


def parse_article(url):
    content = requests.get(url).content.decode("utf-8")

    if "信息学部" in content and "停水" in content:
        soup = BeautifulSoup(content, "lxml")
        return soup.select(".c_content")[0].text
    return None


def modify_last_article(new_last):
    file = codecs.open("lastArticle.py", "w", "utf-8")
    file.write('last_article = "' + new_last + '"')
    file.close()


tzgg_url = "http://www.whu.edu.cn/tzgg.htm"

r = requests.get(tzgg_url)
soup = BeautifulSoup(r.content, "lxml")
list = soup.select("ul.article > li")
today = datetime.datetime.today()


first_article = None
for item in list:
    attrs = item.select("center div")

    # 如果是标题
    if len(attrs) == 0:
        continue

    href = item.select("div > a")[0]

    article__url = "http://www.whu.edu.cn/" + href['href']
    article_title = href.text.strip()

    # 如果循环到上次遍历的地方，则退出
    if first_article == None:
        first_article = article_title

    if article_title == last_article:
        break

    time_text = attrs[1].text
    article_time = datetime.datetime.strptime(time_text, "%Y-%m-%d")

    # 如果不是今天的新闻，则退出
    if today > article_time:
        break

    if "水" in article_title:
        content = parse_article(article__url)
        if content is None:
            continue
        for user in accouts:
            print(str(article_time) + "停水")
            sendMail(user['email'], "停水通知", content)

if first_article != last_article:
    modify_last_article(first_article)
