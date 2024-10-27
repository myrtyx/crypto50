import os
import time
import requests
import json
import pandas as pd
from datetime import datetime

def get_cex_tokens():
    url_bybit = "https://api.bybit.com/v2/public/symbols"
    url_binance = "https://api.binance.com/api/v3/exchangeInfo"
    url_okx = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

    bybit_response = requests.get(url_bybit).json()
    binance_response = requests.get(url_binance).json()
    okx_response = requests.get(url_okx).json()

    bybit_symbols = {symbol['base_currency'] for symbol in bybit_response.get('result', [])}
    binance_symbols = {symbol['baseAsset'] for symbol in binance_response.get('symbols', [])}
    okx_symbols = {ticker['instId'].split('-')[0] for ticker in okx_response.get('data', [])}

    all_tokens = binance_symbols | bybit_symbols | okx_symbols
    token_exchange_map = {
        token: [
            exchange for exchange, symbols in [
                ('Binance', binance_symbols),
                ('Bybit', bybit_symbols),
                ('OKX', okx_symbols)
            ] if token in symbols
        ]
        for token in all_tokens
    }
    return token_exchange_map

def get_top_cryptos_with_fdv():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    all_data = []
    for page in range(1, 3):
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 100,
            'page': page,
            'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            all_data.extend(response.json())
        else:
            print(f"Не удалось получить данные от CoinGecko. Код статуса: {response.status_code}")
        time.sleep(0.1)
    return all_data

def generate_data():
    cex_tokens_data = get_cex_tokens()
    top_cryptos_data = get_top_cryptos_with_fdv()
    stablecoin_symbols = {
        'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDP', 'GUSD', 'USDD',
        'FEI', 'SUSD', 'MIM', 'FRAX', 'LUSD', 'UST', 'EURS', 'HUSD',
        'PAX', 'EURT', 'FDUSD'
    }

    processed_data = []
    for coin in top_cryptos_data:
        if not isinstance(coin, dict):
            continue

        symbol = coin.get('symbol', '').upper()
        if symbol in stablecoin_symbols or not coin.get('fully_diluted_valuation'):
            continue
        valid_list = cex_tokens_data.get(symbol, [])
        if not valid_list:
            continue

        coin_data = {
            'Image': coin.get('image', ''),
            'Name': coin.get('name', ''),
            'Symbol': symbol,
            'Price': coin.get('current_price', 0),
            'MarketCap': coin.get('market_cap', 0),
            'FDV': coin.get('fully_diluted_valuation', 0),
            'CEX': ', '.join(valid_list),
            'M Rank': coin.get('market_cap_rank', 0)
        }
        processed_data.append(coin_data)
        if len(processed_data) >= 300:
            break

    if not processed_data:
        print("Нет данных для обработки.")
        return []

    df = pd.DataFrame(processed_data)

    if 'FDV' in df.columns:
        df['FDV'] = pd.to_numeric(df['FDV'], errors='coerce').fillna(0)
    else:
        print("Столбец 'FDV' отсутствует в DataFrame.")

    df.sort_values('FDV', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.insert(0, 'Rank', df.index)

    required_columns = ['Image', 'Rank', 'Name', 'Symbol', 'Price', 'MarketCap', 'FDV', 'CEX', 'M Rank']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Отсутствуют столбцы в DataFrame: {missing_columns}")

    return df[required_columns].to_dict(orient='records')

def save_current_data():
    data = generate_data()
    with open('current_data.json', 'w') as f:
        json.dump(data, f)

def save_snapshot(data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join('snapshots', f'data_snapshot_{timestamp}.json')
    with open(filename, 'w') as f:
        json.dump(data, f)

def main():
    os.makedirs('snapshots', exist_ok=True)
    while True:
        try:
            data = generate_data()
            with open('current_data.json', 'w') as f:
                json.dump(data, f)
            save_snapshot(data)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        time.sleep(300)

if __name__ == '__main__':
    main()
