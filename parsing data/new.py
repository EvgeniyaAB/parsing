import bs4
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import codecs
import lxml
import json
from tqdm import tqdm



def connect(url):
    headers_data = Headers(headers='firefox', os='win').generate()
    responce = requests.get(url=url, headers=headers_data)
    html_data = responce.text
    return html_data

def vacancy_hh(html_data, url):
    tag_soup = bs4.BeautifulSoup(html_data, 'lxml')
    pages_count = int(tag_soup.find('div', class_='pager').find_all('span', recursive=False)[-1].find('a').text)
    vacanсies = []
    for page in (0, pages_count):
        url_1 = f'{url}&page={page}'
        headers_data = Headers(headers='firefox', os='win').generate()
        responce = requests.get(url=url_1, headers=headers_data)
        html_data = responce.text

        tag_soup = bs4.BeautifulSoup(html_data, 'lxml')
        tag_1 = tag_soup.find_all('div', class_='serp-item')
        for name in tag_1:
            name_vacancy = name.find('h3').text# название вакансии

            a_link = name.find('a')
            link = a_link['href']  # ссылка на вакансию
            b_salary = name.find('span', 'bloko-header-section-3')
            if b_salary is None:
                continue
            salary = b_salary.text.replace('\u202f', '')  # зп
            company = name.find('div', class_='vacancy-serp-item__meta-info-company').text.split(',')[0]
            cities = name.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
            for city in cities:
                city_n = city
                break

            vacansy = {
                    'name': name_vacancy,
                    'company':company,
                    'salary': salary,
                    'link': link,
                    'city': city_n
                    }

            vacanсies.append(vacansy)
        else:
            continue
    return vacanсies

def vacanсies_viborka(vacanсies, a, b):
    vacanсies_viborka = []
    for vac in vacanсies:
            if a in vac['name'] or b in vac['name']:
                vacanсies_viborka.append(vac)
            else:
                continue
    return vacanсies_viborka


if __name__ == '__main__':
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    vacanсies_viborka(vacancy_hh(connect(url), url), 'Flask', 'Django')
    filename_vacancys = 'data.json'
    with open(filename_vacancys, 'w', encoding='utf-8') as f:
        json.dump(vacanсies_viborka(vacancy_hh(connect(url), url), 'Flask', 'Django'), f, indent=4, ensure_ascii=False)
        for i in tqdm(filename_vacancys):
            time.sleep(1)

