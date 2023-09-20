import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('output.xlsx')

# Просмотр первых строк данных
print(data.head())

# Общая информация о данных
print(data.info())

# Основные статистические показатели
print(data.describe())

# гистограммы
plt.hist(data['Административный район'], bins=20, color='skyblue')
plt.xlabel('Административный район')
plt.xticks(rotation=90, fontsize=5)
plt.ylabel('Частота')
plt.show()
plt.hist(data['Регион РФ'], color='skyblue')
plt.xlabel('Регион РФ')
plt.xticks(rotation=90, fontsize=5)
plt.ylabel('Частота')
plt.show()
plt.hist(data['Плановое начало отключения Время'], color='skyblue')
plt.xlabel('Плановое начало отключения Время')
plt.xticks(rotation=90, fontsize=5)
plt.ylabel('Частота')
plt.show()
plt.hist(data['Плановое восстановление Время'], color='skyblue')
plt.xlabel('Плановое восстановление Время')
plt.xticks(rotation=90, fontsize=5)
plt.ylabel('Частота')
plt.show()
