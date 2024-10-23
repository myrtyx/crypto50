import requests
import json
import time


# Функция для получения данных о криптовалютах с их FDV
def get_top_cryptos_with_fdv(limit=200):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    
    all_data = []  # List to store all the data
    
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
            page_data = response.json()  # Get the JSON response
            all_data.extend(page_data)   # Add data from the current page to the list
        elif response.status_code == 429:
            print("Превышен лимит запросов. Ждем 10 секунд перед повторной попыткой...")
            time.sleep(0.1)  # Ожидание 0.2 секунд
            response = requests.get(url, params=params)
            if response.status_code == 200:
                page_data = response.json()
                all_data.extend(page_data)
        else:
            print(f"Ошибка получения данных для страницы {page}: {response.status_code}")

    jsontable = json.dumps(all_data, indent=4)
    # Print the full JSON data of both pages
    return jsontable  # Pretty-print the JSON data
     
def table_fdv():
    jsontable = get_top_cryptos_with_fdv(limit=200)
    data = json.loads(jsontable)

    all_table = []
    for token in data:
        table = {
            'symbol': token['symbol'],
            'name': token['name'],
            'image': token['image'],
            'current_price': token['current_price'],
            'market_cap': token['market_cap'],
            'market_cap_rank': token['market_cap_rank'],
            'fully_diluted_valuation': token.get('fully_diluted_valuation')  # Using .get() in case the value is missing
        }
        all_table.append(table)
    print(f"Total tokens collected: {len(all_table)}")
    final_json=json.dumps(all_table, indent=4)

    with open('table_fdv.json', "w") as f:
        json.dump(all_table, f, indent=4)



if __name__ == "__main__":
    table_fdv()
