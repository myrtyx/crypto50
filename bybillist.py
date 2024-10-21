import requests
import csv

# Запрос для получения всей информации о торговых парах Bybit
url = "https://api.bybit.com/v2/public/symbols"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Получаем список уникальных токенов (base_currency)
    symbols = {symbol['base_currency'] for symbol in data['result']}
    
    # Создаем CSV файл и записываем в него данные
    with open('bybit_tokens.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Token"])  # Заголовок
        for symbol in sorted(symbols):
            writer.writerow([symbol])
    
    print(f"Всего доступных токенов на Bybit: {len(symbols)}")
    print("Данные успешно записаны в 'bybit_tokens.csv'")
else:
    print(f"Ошибка получения данных: {response.status_code}")
