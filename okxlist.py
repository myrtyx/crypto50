import requests
import csv

# Запрос для получения всей информации о торговых парах OKX
url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Проверим структуру данных и правильный ключ
    try:
        symbols = {ticker['instId'].split('-')[0] for ticker in data['data']}
    except KeyError as e:
        print(f"Ключ '{e}' не найден в данных.")
        symbols = set()

    # Создаем CSV файл и записываем в него данные
    with open('okx_tokens.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Token"])  # Заголовок
        for symbol in sorted(symbols):
            writer.writerow([symbol])
    
    print(f"Всего доступных токенов на OKX: {len(symbols)}")
    print("Данные успешно записаны в 'okx_tokens.csv'")
else:
    print(f"Ошибка получения данных: {response.status_code}")
