import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.google.com/finance/quote/'

# stock
# position = stock * quantity
# portfolio = position + allocation

portfolio = [
    {
    'ticker': 'BNS',
    'exchange': 'TSE',
    'quantity': 100
    },
    {
    'ticker': 'GOOGL',
    'exchange': 'NASDAQ',
    'quantity': 30
    },
    {
    'ticker': 'SHOP',
    'exchange': 'TSE',
    'quantity': 10
    },
    {
    'ticker': 'MSFT',
    'exchange': 'NASDAQ',
    'quantity': 2
    }
]

def get_price(mainElement):
    return float(mainElement.attrs['data-last-price'])

def convert_currency(price, currency):
    response = requests.get(f"{BASE_URL}{currency}-USD")
    soupResp = BeautifulSoup(response.content, 'html.parser')
    value = float(soupResp.find('div', attrs={'data-target': 'USD'}).attrs['data-last-price'])
    return round(price * value,2) 

resp = requests.get(f"{BASE_URL}{portfolio[0]['ticker']}:{portfolio[0]['exchange']}")

soup = BeautifulSoup(resp.content, 'html.parser')

mainElement = soup.find('div', attrs={'data-exchange': portfolio[0]['exchange']})

price = get_price(mainElement)

currency = mainElement.attrs['data-currency-code']

print(f"price: {price} {currency}")

if currency != 'USD':
    price = convert_currency(price, currency)

print(f"USD price: {price} USD")