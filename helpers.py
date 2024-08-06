import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
import pandas as pd
import constants as c
import data_classes

## Check if currency code is correct and store it in PREF_CURRNECY constant
def check_currency(currency):
    with open('currencies.csv', newline='') as csvfile:
        input_reader = csv.reader(csvfile)
        found = False
        for row in input_reader:
            if row[0] == currency:
                found = True
                break
        if not found:
            print('Please check currency code and try again!')
            exit()

        c.PREF_CURRENCY = currency


## Read stock data the user entered in positions_input.csv file and store it in correspoding variables
def read_input():
    with open('positions_input.csv', newline='') as csvfile:
        input_reader = csv.reader(csvfile)
        positions = []

        for row in input_reader:
            if input_reader.line_num != 1:
                ticker = row[0].replace(" ", "")
                exchange = row[1].replace(" ", "")
                quantity = int(row[2])
                positions.append(data_classes.Position(data_classes.Stock(ticker,exchange),quantity))

        return positions


## Retrieve the price as a float from the web element
def get_price(mainElement):
    return float(mainElement.attrs['data-last-price'])


## Convert currency to the prefered currency specified by user
def convert_currency(price, currency):
    response = requests.get(f"{c.BASE_URL}{currency}-{c.PREF_CURRENCY}")
    soupResp = BeautifulSoup(response.content, 'html.parser')
    value = float(soupResp.find('div', attrs={'data-target': c.PREF_CURRENCY}).attrs['data-last-price'])
    return round(price * value,2) 


## Retrieve price from web element and return stock information as a dictionary
def get_price_information(ticker, exchange):
    resp = requests.get(f"{c.BASE_URL}{ticker}:{exchange}")
    soup = BeautifulSoup(resp.content, 'html.parser')
    mainElement = soup.find('div', attrs={'data-exchange': exchange})

    price = get_price(mainElement)

    currency = mainElement.attrs['data-currency-code']

    pref_price = price
    if currency != c.PREF_CURRENCY:
        pref_price = convert_currency(price, currency)

    return{
        'ticker': ticker,
        'exchange': exchange,
        'price': price,
        'currency': currency,
        'pref_price': pref_price
    }


## Save the portfolio to csv file, form a table from the portfolio data and display it to the user
def display_summary(portfolio):
    if not isinstance(portfolio, data_classes.Portfolio):
        raise TypeError('Please provide a Portfolio type variable!')

    total_value = portfolio.get_total_value()
    positions_data = []

    for position in portfolio.positions:
        market_value = position.quantity * position.stock.pref_price

        positions_data.append({
            'Ticker': position.stock.ticker,
            'Exchange': position.stock.exchange,
            'Quantity': position.quantity,
            'Price': position.stock.pref_price,
            'Market Value': market_value,
            '% Allocation': round(market_value / total_value * 100,2)
        })
    
    positions_data = sorted(positions_data, key=lambda x: x['Market Value'], reverse=True)

    # Display summary table
    print(tabulate(positions_data,
            headers='keys',
            tablefmt='psql',
            floatfmt='.2f'))

    print(f'\nTotal portfolio value: {c.PREF_CURRENCY} {total_value:,.2f}')

    # Output summary to porfolio csv file
    positions_data.append({'Total portfolio value': f'{c.PREF_CURRENCY} {total_value:,.2f}'})
    df = pd.DataFrame(positions_data)
    df.to_csv(c.FILE_NAME, index=False)
