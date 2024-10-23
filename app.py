from flask import Flask, jsonify
import json
import re
import pandas as pd

app = Flask(__name__)

def process_data():
    # Load cex_tokens.json
    with open('cex_tokens.json', 'r') as f:
        cex_tokens_data = json.load(f)
    
    # Normalize symbols in cex_tokens_data
    normalized_cex_tokens = {}
    for symbol, exchanges in cex_tokens_data.items():
        # Normalize token symbol by stripping numeric prefixes and converting to uppercase
        normalized_symbol = re.sub(r'^\d+', '', symbol).upper()
        if normalized_symbol in normalized_cex_tokens:
            # If symbol already exists, extend the list of exchanges
            normalized_cex_tokens[normalized_symbol].extend(exchanges)
        else:
            normalized_cex_tokens[normalized_symbol] = exchanges

    # Remove duplicates in exchanges list
    for symbol in normalized_cex_tokens:
        normalized_cex_tokens[symbol] = list(set(normalized_cex_tokens[symbol]))

    # Load table_fdv.json
    with open('table_fdv.json', 'r') as f:
        top_cryptos_data = json.load(f)
    
    # Set of stablecoin symbols to exclude
    stablecoin_symbols = {'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDP', 'GUSD', 'USDD', 'FEI',
                          'SUSD', 'MIM', 'FRAX', 'LUSD', 'UST', 'EURS', 'HUSD', 'PAX', 'EURT', 'FDUSD'}

    # Desired number of entries in the table
    desired_number_of_coins = 300  # You can adjust this as needed

    # Process the data
    processed_data = []
    for coin in top_cryptos_data:
        image = coin.get('image')
        symbol = coin['symbol'].upper()
        name = coin['name']
        price = coin['current_price']
        market_cap = coin['market_cap']
        fdv = coin.get('fully_diluted_valuation')
        market_cap_rank = coin.get('market_cap_rank')

        # Skip coins without FDV
        if fdv is None or fdv == 0:
            continue

        # Exclude stablecoins
        if symbol in stablecoin_symbols:
            continue

        # Check which exchanges the coin is traded on
        valid_list = normalized_cex_tokens.get(symbol, [])

        # If token is not listed on any exchange, skip it
        if not valid_list:
            continue

        cex_str = ', '.join(valid_list)

        # Build a dict with the required data
        coin_data = {
            'Image': image,
            'Name': name,
            'Symbol': symbol,
            'Price': price,
            'MarketCap': market_cap,
            'FDV': fdv,
            'CEX': cex_str,
            'M Rank': market_cap_rank  # Add the 'M Rank' field here
        }
        processed_data.append(coin_data)

        # Stop if we've collected the desired number of coins
        if len(processed_data) >= desired_number_of_coins:
            break

    # Create a DataFrame
    df = pd.DataFrame(processed_data)

    # Convert FDV to numeric and handle missing values
    df['FDV'] = pd.to_numeric(df['FDV'], errors='coerce').fillna(0)

    # Sort by FDV descending to get rank
    df.sort_values('FDV', ascending=False, inplace=True)

    # Reset index to get Rank
    df.reset_index(drop=True, inplace=True)
    df.index += 1  # Start rank from 1
    df.insert(0, 'Rank', df.index)

    # Select relevant columns
    result_data = df[['Image', 'Rank', 'Name', 'Symbol', 'Price', 'MarketCap', 'FDV', 'CEX', 'M Rank']].to_dict(orient='records')

    return result_data

@app.route('/api/data')
def get_data():
    data = process_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
