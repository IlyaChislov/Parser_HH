import re

import bs4
import fake_headers
import requests


def gen_headers():
    headers_gen = fake_headers.Headers(os="win", browser="Chrome")
    return headers_gen.generate()


def main_function():
    url = 'https://spb.hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page=0'

    response = requests.get(url, headers=gen_headers())
    main_html = response.text
    soup = bs4.BeautifulSoup(main_html, 'lxml')
    return soup


def fun_count_page(soup):
    count_pages_tags = soup.find_all("span", class_="pager-item-not-in-short-range")
    count_page = int(count_pages_tags[-1].find("span").text.strip())
    return count_page


def load_info(soup_vacancy):
    company_tag = soup_vacancy.find("div", class_="vacancy-company-redesigned")
    if company_tag is not None:
        company = company_tag.find("span", class_="bloko-header-section-2").text.strip()
        company = re.sub("\xa0", "", company)
    print(company)
    town_tag = soup_vacancy.find("p", attrs={'data-qa': 'vacancy-view-location'})
    if town_tag is None:
        town_tag = soup_vacancy.find('span', attrs={'data-qa': 'vacancy-view-raw-address'})
    town = town_tag.text.strip()
    print(town)
    salary_tag = soup_vacancy.find("div", attrs={'data-qa': 'vacancy-salary'})
    if salary_tag is None:
        salary = "По результатам собеседования"
    else:
        pattern = "\xa0000"
        salary = re.sub(pattern, "", salary_tag.text.strip())
    result = {"Компания": company, "Адрес": town, "Зарплата": salary}
    return result
