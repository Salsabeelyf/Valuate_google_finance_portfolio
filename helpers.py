import requests
from bs4 import BeautifulSoup
import constants as c


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