import requests
import json
import re
import pandas as pd
import time

# Получение списка токенов с бирж
def get_cex_tokens():
    # Загрузка данных с трех бирж
    url_bybit = "https://api.bybit.com/v2/public/symbols"
    url_binance = "https://api.binance.com/api/v3/exchangeInfo"
    url_okx = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"

    bybit_symbols = {symbol['base_currency'] for symbol in requests.get(url_bybit).json()['result']}
    binance_symbols = {symbol['baseAsset'] for symbol in requests.get(url_binance).json()['symbols']}
    okx_symbols = {ticker['instId'].split('-')[0] for ticker in requests.get(url_okx).json()['data']}

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

# Получение данных с FDV
def get_top_cryptos_with_fdv(limit=200):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    all_data = []
    for page in range(1, 3):
        params = {
            'vs_currency': 'usd', 'order': 'market_cap_desc', 'per_page': 100,
            'page': page, 'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        all_data.extend(response.json())
        time.sleep(0.3)
    return all_data

def generate_data():
    cex_tokens_data = get_cex_tokens()
    top_cryptos_data = get_top_cryptos_with_fdv()
    stablecoin_symbols = {'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDP', 'GUSD', 'USDD', 'FEI',
                          'SUSD', 'MIM', 'FRAX', 'LUSD', 'UST', 'EURS', 'HUSD', 'PAX', 'EURT', 'FDUSD'}

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
        print("No data to process.")
        return []

    df = pd.DataFrame(processed_data)

    # Проверяем наличие 'FDV' перед преобразованием
    if 'FDV' in df.columns:
        df['FDV'] = pd.to_numeric(df['FDV'], errors='coerce').fillna(0)
    else:
        print("Column 'FDV' is missing from DataFrame.")

    df.sort_values('FDV', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.insert(0, 'Rank', df.index)

    required_columns = ['Image', 'Rank', 'Name', 'Symbol', 'Price', 'MarketCap', 'FDV', 'CEX', 'M Rank']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

    return df[required_columns].to_dict(orient='records')


