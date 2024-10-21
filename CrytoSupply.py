import requests
import csv

# Функция для получения данных о криптовалютах с их FDV
def get_top_cryptos_with_fdv(limit=200):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    cryptos = []
    for page in range(1, 3):  # Две страницы по 100 криптовалют
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': page,
            'sparkline': 'false'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            cryptos.extend(response.json())
        else:
            print(f"Ошибка получения данных для страницы {page}: {response.status_code}")
    
    return cryptos

# Функция для записи данных в CSV файл
def write_to_csv(data, filename="top_cryptos_fdv.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Symbol", "Name", "Price" ,"Market Cap (USD)", "FDV (USD)"])

        for idx, coin in enumerate(data, start=1):
            symbol = coin.get('symbol', 'N/A').upper()
            name = coin.get('name', 'N/A')
            price = coin.get('current_price', 'N/A')
            market_cap = coin.get('market_cap', 'N/A')
            fdv = coin.get('fully_diluted_valuation', 'N/A')
            writer.writerow([idx, symbol, name, price, market_cap, fdv])

        print(f"Данные успешно записаны в файл: {filename}")

# Основная функция для выполнения программы
def main():
    top_cryptos = get_top_cryptos_with_fdv(limit=200)
    if top_cryptos:
        write_to_csv(top_cryptos)
    else:
        print("Не удалось получить данные.")

if __name__ == "__main__":
    main()
