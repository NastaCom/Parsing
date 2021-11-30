import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
#import pandas as pd


specialist = input('Введите необходимую вакансию: ')
page = 0
next_page = True
while True:

    url = 'https://spb.hh.ru' # /search/vacancy?clusters=true&area=2&ored_clusters=true&enable_snippets=true&salary=&text=data+analyst

    params = {'text': specialist, 'page': page}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    try:
        page_next = dom.find('div', {'class': ['pager']}).find('a', {'class': ['bloko-button']}).get('href')
    except:
        next_page = False
        break

    vacancies = dom.find_all('div', {'class', 'vacancy-serp-item'})

    vacancies_list = []
    for vacance in vacancies:
        vacance_data = {}
        name = vacance.find('a')
        link = name.get('href')
        name = name.text

        try:
            salary = vacance.find('div', {'class': 'vacancy-serp-item__sidebar'}).find('span').text.replace('\u202f', ' ')
            salary_str = salary[-4:]
            salary = salary[:-4]
            if '–' in salary:
                salary_list = salary.split('–')
                salary_min = int(salary_list[0].replace(' ', ''))
                salary_max = int(salary_list[1].replace(' ', ''))
            elif salary[:2] == 'от':
                salary_min = salary
                salary_max = None
            elif salary[:2] == 'до':
                salary_min = None
                salary_max = salary
        except:
            salary = None
            salary_str = None
            salary_min = None
            salary_max = None

        vacance_data['name'] = name
        vacance_data['link'] = link
        vacance_data['salary_min'] = salary_min
        vacance_data['salary_max'] = salary_max
        vacance_data['salary_str'] = salary_str
        vacance_data['hh_spb'] = url

        vacancies_list.append(vacance_data)

    params['page'] += 1

    with open('hh_vacance.json', 'w', encoding='utf-8') as hh:
        json.dump(vacancies_list, hh)

    pprint(vacancies_list)

