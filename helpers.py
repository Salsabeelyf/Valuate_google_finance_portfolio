import requests
from bs4 import BeautifulSoup
import constants as c
from tabulate import tabulate
import data_classes

def get_price(mainElement):
    return float(mainElement.attrs['data-last-price'])

def convert_currency(price, currency):
    response = requests.get(f"{c.BASE_URL}{currency}-USD")
    soupResp = BeautifulSoup(response.content, 'html.parser')
    value = float(soupResp.find('div', attrs={'data-target': 'USD'}).attrs['data-last-price'])
    return round(price * value,2) 

def get_price_information(ticker, exchange):
    resp = requests.get(f"{c.BASE_URL}{ticker}:{exchange}")
    soup = BeautifulSoup(resp.content, 'html.parser')
    mainElement = soup.find('div', attrs={'data-exchange': exchange})

    price = get_price(mainElement)

    currency = mainElement.attrs['data-currency-code']

    usd_price = price
    if currency != 'USD':
        usd_price = convert_currency(price, currency)

    return{
        'ticker': ticker,
        'exchange': exchange,
        'price': price,
        'currency': currency,
        'usd_price': usd_price
    }

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
            position.stock.usd_price,
            position.quantity * position.stock.usd_price,
            position.quantity * position.stock.usd_price / total_value * 100
        ])

    print(tabulate(sorted(positions_data, key=lambda x: x[4], reverse=True),
             headers=['Ticker', 'Exchange', 'Quantity', 'Price', 'Market Value', '% Allocation'],
             tablefmt='psql',
             floatfmt='.2f'))

    print(f'Total portfolio value: ${total_value:,.2f}')
