"""
1. Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные данные в БД
"""


import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime, date, time



#dbcol - ссылка на коллекцию в Mongo
#ident: строка-критерий

def new_news(dbcol, ident):

    if dbcol.find_one({'title': ident}) == None:
        return False
    else:
        return True

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

news = []

sites = [
    {"site": "https://news.mail.ru/",
     "title": "//td[@class='daynews__main']//span[1]/text() | //div[@class='daynews__item']//span/text() | //li[@class='list__item']/a/text()",
     "link": "//td[@class='daynews__main']//a/@href | //div[@class='daynews__item']/a/@href | //li[@class='list__item']/a/@href",
     "date": "//td[@class='daynews__main']//a/@href | //div[@class='daynews__item']/a/@href | //li[@class='list__item']/a/@href"},
    {"site": "https://lenta.ru",
     "title": "//div[@class='span4']/div[@class='item']/a/text() | //div[@class='first-item']/h2/a/text()",
     "link": "//div[@class='span4']/div[@class='item']/a/@href | //div[@class='first-item']/h2/a/@href",
     "date": "//div[@class='item']/a/time/@datetime | //div[@class='first-item']/h2/a/time/@datetime"},
    {"site": "https://yandex.ru/news/",
     "title": "//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//h2/text()",
     "link": "//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//span/a/@href",
     "date": "//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']//span[@class='mg-card-source__time']/text()"}
]

for site in sites:
    main_link = site["site"]

    responce = requests.get(main_link, headers=header)
    dom = html.fromstring(responce.text)

    title = dom.xpath(site["title"])
    link = dom.xpath(site["link"])
    date = dom.xpath(site["date"])


    i = 0
    for item in title:
        if main_link == "https://lenta.ru":

            date[i] = datetime.strptime(str(datetime.now().date()) + date[i].split(',')[0], "%Y-%m-%d %H:%M")

            if not link[i].startswith('https'):
                link[i] = 'https://lenta.ru' + link[i]

        if main_link == "https://news.mail.ru/":

            date[i] = datetime.now()

        if main_link == "https://yandex.ru/news/":

            date[i] = datetime.strptime(str(datetime.now().date()) + str(date[i]), '%Y-%m-%d%H:%M')

        news_data = {}
        news_data['title'] = title[i]
        news_data['link'] = link[i]
        news_data['date'] = date[i]
        news_data['site'] = main_link


        if new_news(db.news, news_data['title']) == False:
            news.append(news_data)

        i += 1

if news:
    pprint(news)
    db.news.insert_many(news)


