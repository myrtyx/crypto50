import requests
import json

def main():
    url = "https://api.bybit.com/v2/public/symbols"
    bybit_response = requests.get(url)

    url = "https://api.binance.com/api/v3/exchangeInfo"
    binance_response = requests.get(url)

    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    oks_response = requests.get(url)


    if bybit_response.status_code == 200:
        data = bybit_response.json()
        # Получаем список уникальных токенов (base_currency)
        bybit_symbols = {symbol['base_currency'] for symbol in data['result']}
        print(len(bybit_symbols))
    else:
        print(f"Ошибка получения данных: {bybit_response.status_code}")


    if binance_response.status_code == 200:
        data = binance_response.json()
        # Получаем список уникальных токенов (baseAsset)
        binance_symbols = {symbol['baseAsset'] for symbol in data['symbols']}
        print(len(binance_symbols))
    else:
        print(f"Ошибка получения данных: {binance_response.status_code}")


    if oks_response.status_code == 200:
        data = oks_response.json()
        
        # Проверим структуру данных и правильный ключ
        try:
            okx_symbols = {ticker['instId'].split('-')[0] for ticker in data['data']}
        except KeyError as e:
            print(f"Ключ '{e}' не найден в данных. (OKX)")
            okx_symbols = set()
        print(len(okx_symbols))
    else:
        print(f"Ошибка получения данных: {oks_response.status_code}")


    all_tokens = binance_symbols | bybit_symbols | okx_symbols
    token_exchange_map = {}

    for token in all_tokens:
        valid_list = []
        if token in binance_symbols:
            valid_list.append('Binance')
        if token in bybit_symbols:
            valid_list.append('Bybit')
        if token in okx_symbols:
            valid_list.append('OKX')
        token_exchange_map[token] = valid_list

    sorted_token_exchange_map = dict(sorted(token_exchange_map.items()))

    with open('cex_tokens.json', 'w') as json_file:
        json.dump(sorted_token_exchange_map, json_file, indent=4)