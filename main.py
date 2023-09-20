import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time

# подсчет общего числа страниц
def all_pages():
    all_a_elements = soup.find_all('a')  # все элементы <a> на странице

    target_elements = filter(
        lambda a: a.has_attr('href') and 'PAGEN_1' in a['href'], all_a_elements  # lambda функцию для фильтрации элементов
    )
    found_el = []

    for element in target_elements:
        if element.has_attr('style') and 'text-decoration: none; font-size: 25px;' in element['style']:
            found_el.append(element)
    html_string = str(found_el[1])

    pattern = r'\?PAGEN_1=(\d+)' # шаблон для поиска числа в атрибуте href
    match = re.search(pattern, html_string)
    if match:
        number = match.group(1)
        return int(number)
    else:
        print("Число не найдено в строке.")

while True:
    # данные для фильтрации элементов по дате
    date_from_str = '20-09-2023'
    date_to_str = '27-09-2023'
    date_from = datetime.strptime(date_from_str, '%d-%m-%Y')
    date_to = datetime.strptime(date_to_str, '%d-%m-%Y')

    # URL и параметры запроса
    base_url = 'https://rosseti-lenenergo.ru/planned_work/'
    params = {'PAGEN_1': 1}

    # DataFrame для данных со всех страниц.
    all_data = pd.DataFrame()

    while True:
        response = requests.get(base_url, params=params)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        pages = all_pages()

        table = soup.find('table', class_='tableous_facts funds')  # поиск таблицы 'tableous_facts funds'
        columns = ['Регион РФ', 'Административный район', 'Населённый пункт', 'Улица',
                   'Плановое начало отключения Дата', 'Плановое начало отключения Время',
                   'Плановое восстановление Дата', 'Плановое восстановление Время', 'Филиал', 'РЭС', 'Комментарий']
        data_by_column = {column: [] for column in columns}

        for row in table.find_all('tr')[1:]:  # без первой строки, т.к. это заголовки столбцов
            columns_data = row.find_all('td')
            if len(columns_data) > 4:  # проверка, чтобы было хотя бы три элемента в строке
                third_element = columns_data[4].get_text().strip()
                if pd.to_datetime(third_element, dayfirst=True) >= date_from and pd.to_datetime(third_element, dayfirst=True) <= date_to:   # сравнить значение третьего элемента
                    for i, column in enumerate(columns_data):
                        data_by_column[columns[i]].append(column.get_text().strip())
        current_data = pd.DataFrame(data_by_column)
        all_data = pd.concat([all_data, current_data], ignore_index=True)

        # Проверка наличия следующей страницы, если она есть
        next_page = soup.find('a', class_='next')
        if next_page:
            params['PAGEN_1'] += 1
            print(params['PAGEN_1'])
            print(pages)
            if params['PAGEN_1'] == (pages+1):
                break
        else:
            break

    all_data.to_csv('данные.csv', encoding='utf-8', index=False, sep=';')
    all_data.to_excel('output.xlsx',  index=False)
    time.sleep(60)
