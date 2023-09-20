import pandas as pd
import requests
import csv

csv_data = []
file_path = 'streets.xlsx'  # путь к файлу с улицами
sheet_name = 'Sheet1'

df = pd.read_excel(file_path, sheet_name=sheet_name)
column_data = df.values

for column in column_data:
    adress = column
    url = f'https://geocode.gate.petersburg.ru/parse/free?street={adress}'
    headers = {'accept': 'application/json'}  # заголовок для получения ответа в формате JSON

    response = requests.get(url, headers=headers)  # GET-запрос

    if response.status_code == 200: # проверка успешности запроса
        data = response.json()
        if 'Building_ID' in data:
            building_id = data['Building_ID']
            name = data['Name']
            appending = [name, building_id]
            csv_data.append(appending)
        else:
            print("Ключ 'Building_ID' не найден в JSON-ответе.")
            appending = [adress, 'Не найдено']
            csv_data.append(appending)
    else:
        print(f"Ошибка запроса: {response.status_code}")

with open('outputNew.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for row in csv_data:
        writer.writerow(row)
