import requests
import csv

# Запрос для получения всей информации о торговых парах
url = "https://api.binance.com/api/v3/exchangeInfo"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Получаем список уникальных токенов (baseAsset)
    symbols = {symbol['baseAsset'] for symbol in data['symbols']}
    
    # Создаем CSV файл и записываем в него данные
    with open('binance_tokens.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Token"])  # Заголовок
        for symbol in sorted(symbols):
            writer.writerow([symbol])
    
    print(f"Всего доступных токенов: {len(symbols)}")
    print("Данные успешно записаны в 'binance_tokens.csv'")
else:
    print(f"Ошибка получения данных: {response.status_code}")
