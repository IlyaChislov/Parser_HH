import bs4
import requests
import json
from function import main_function, gen_headers, load_info, fun_count_page

# <div data-qa="vacancy-serp__results" id="a11y-main-content"
# <div class="serp-item vacancy-serp-item_clickme serp-item_link serp-item-redesign"
# <div class="serp-item serp-item_link serp-item-redesign"
# <span class="tertiary-link--sh6yIH1ylrRhVPtd1i6a serp-item__title-link serp-item__title-link_redesign" data-qa="serp-item__title">Разработчик Python (парсинг и сервисы синхронизации)</span>
# <div class="bloko-v-spacing bloko-v-spacing_base-5"></div>

data = []
soup = main_function()
count_page = fun_count_page(soup)
url = 'https://spb.hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page='
for page in range(count_page):
    print(f"Страница {page}")
    url += f"{page}"
    response = requests.get(url, headers=gen_headers())
    html = response.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    vacancy_tags_list = soup.find("div", attrs={'data-qa': 'vacancy-serp__results', 'id': 'a11y-main-content'})
    if vacancy_tags_list is None:
        continue
    vacancy_tags = vacancy_tags_list.find_all("div", class_="serp-item_link")
    for vacancy in vacancy_tags:
        a_tag = vacancy.find("a", class_="bloko-link")
        link_relative = a_tag["href"]
        vacancy_html = requests.get(link_relative, headers=gen_headers()).text
        soup_vacancy = bs4.BeautifulSoup(vacancy_html, 'lxml')
        description = soup_vacancy.find("div", class_="vacancy-description")
        if description is None:
            continue
        description = description.text.strip()
        if "Django" in description and "Flask" in description:
            print(link_relative)
            dict_vacancy = load_info(soup_vacancy)
            dict_vacancy["Ссылка"] = link_relative
            data.append(dict_vacancy)
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)