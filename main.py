import pandas as pd
import re

# Function to read and normalize exchange tokens
def read_exchange_tokens(filename):
    tokens = set()
    with open(filename, 'r') as csvfile:
        next(csvfile)  # Skip header
        for line in csvfile:
            token = line.strip()
            # Normalize token symbol by stripping numeric prefixes
            normalized_token = re.sub(r'^\d+', '', token)
            tokens.add(normalized_token.upper())
    return tokens

def main():
    # Read the top cryptocurrencies from the CSV file
    top_cryptos_df = pd.read_csv('top_cryptos_fdv.csv', encoding='ISO-8859-1')

    # Read exchange tokens
    binance_tokens = read_exchange_tokens('binance_tokens.csv')
    bybit_tokens = read_exchange_tokens('bybit_tokens.csv')
    okx_tokens = read_exchange_tokens('okx_tokens.csv')
    extra_tokens = read_exchange_tokens('extra.csv')

    # Set of stablecoin symbols to exclude
    stablecoin_symbols = {'USDT', 'USDC', 'DAI', 'BUSD', 'TUSD', 'USDP', 'GUSD', 'USDD', 'FEI',
                          'SUSD', 'MIM', 'FRAX', 'LUSD', 'UST', 'EURS', 'HUSD', 'PAX', 'EURT' , 'FDUSD'}

    # Desired number of entries in the table
    desired_number_of_coins = 300  # You can adjust this as needed

    # Process the data
    processed_data = []
    for index, row in top_cryptos_df.iterrows():
        symbol = row['Symbol'].upper()
        name = row['Name']
        price = row['Price']
        market_cap = row['Market Cap (USD)']
        fdv = row['FDV (USD)']

        # Skip coins without FDV
        if pd.isna(fdv) or fdv == 0:
            continue

        # Exclude stablecoins
        if symbol in stablecoin_symbols:
            continue

        # Check which exchanges the coin is traded on
        valid_list = []
        if symbol in binance_tokens:
            valid_list.append('Binance')
        if symbol in bybit_tokens:
            valid_list.append('Bybit')
        if symbol in okx_tokens:
            valid_list.append('OKX')
        if symbol in extra_tokens:
           valid_list.append('Extra')

        # If token is not listed on any exchange, skip it
        if not valid_list:
            continue

        cex_str = ', '.join(valid_list)

        # Build a dict with the required data
        coin_data = {
            'Name': name,
            'Symbol': symbol,
            'Price': price,
            'MarketCap': market_cap,
            'FDV': fdv,
            'CEX': cex_str
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

    # Output the DataFrame
    print(df[['Rank', 'Name', 'Symbol', 'Price', 'MarketCap', 'FDV', 'CEX']])

    # Write to CSV
    df.to_csv('crypto_index.csv', columns=['Rank', 'Name', 'Symbol', 'Price', 'MarketCap', 'FDV', 'CEX'], index=False)

if __name__ == '__main__':
    main()
