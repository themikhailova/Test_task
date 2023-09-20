import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def all_pages():
    all_a_elements = soup.find_all('a')  # все элементы <a> на странице
    target_elements = filter(
        lambda a: a.has_attr('href') and 'PAGEN_1' in a['href'], all_a_elements  # lambda функция для фильтрации элементов
    )
    found_el = []
    for element in target_elements:
        if element.has_attr('style') and 'text-decoration: none; font-size: 25px;' in element['style']:
            found_el.append(element)
    html_string = str(found_el[1])
    pattern = r'\?PAGEN_1=(\d+)'  # шаблон для поиска числа в атрибуте href
    match = re.search(pattern, html_string)
    if match:
        number = match.group(1)
        return int(number)
    else:
        print("Число не найдено в строке.")


base_url = 'https://rosseti-lenenergo.ru/planned_work/'
params = {'PAGEN_1': 1}

all_data = pd.DataFrame()

while True:
    response = requests.get(base_url, params=params)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    pages = all_pages()
    table = soup.find('table', class_='tableous_facts funds')

    data_list = []  # пустой список для хранения данных

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 3:
            data = columns[3].get_text().strip()
            data_list.append(data)
    current_data = pd.DataFrame(data_list)
    all_data = pd.concat([all_data, current_data], ignore_index=True)

    next_page = soup.find('a', class_='next')
    if next_page:
        params['PAGEN_1'] += 1
        if params['PAGEN_1'] == (pages+1):
            break
    else:
        break

data = []
for data1 in all_data.values:
    for adr in data1:
        data.append(adr.split(','))

street = None
merged_addresses = []
for item1 in data:
    for item in item1:
        if 'ул.' in item or 'пр.' in item  or 'Ул.' in item or 'Пр.' in item or 'Пер.' in item or 'ш' in item or 'п' in item\
                or 'ул' in item or 'пр' in item:
            street = item
        else:
            if 'д.' in item or ('д.' in item and 'лит.' in item) or ('д.' in item and 'лит.' in item and 'корп.' in item):
                merged_addresses.append(street + ' ' + item)
            else:
                merged_addresses.append(item)

df = pd.DataFrame(merged_addresses)
df.to_excel('streets.xlsx', index=False)

