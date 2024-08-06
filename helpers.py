import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
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


## Form a table from the portfolio data and display it to the user
def display_summary(portfolio):
    if not isinstance(portfolio, data_classes.Portfolio):
        raise TypeError('Please provide a Portfolio type variable!')

    total_value = portfolio.get_total_value()
    positions_data = []

    for position in portfolio.positions:
        positions_data.append([
            position.stock.ticker,
            position.stock.exchange,
            position.quantity,
            position.stock.pref_price,
            position.quantity * position.stock.pref_price,
            position.quantity * position.stock.pref_price / total_value * 100
        ])

    print(tabulate(sorted(positions_data, key=lambda x: x[4], reverse=True),
             headers=['Ticker', 'Exchange', 'Quantity', 'Price', 'Market Value', '% Allocation'],
             tablefmt='psql',
             floatfmt='.2f'))

    print(f'Total portfolio value: {c.PREF_CURRENCY} {total_value:,.2f}')
