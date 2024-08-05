from data_classes import *
from helpers import display_summary

def run():

    c.PREF_CURRENCY = input('Hello, Please specify the Output Curreny: ')
    nPositions = int(input('Number of positions: '))
    
    positions = []

    for i in range(0,nPositions):
        print(f'Position {i+1}:')
        ticker = input('Ticker: ')
        exchange = input('Exchange: ')
        quantity = int(input('Quantity: '))
        positions.append(Position(Stock(ticker,exchange),quantity))
    
    portfolio = Portfolio(positions)

    display_summary(portfolio)

if __name__ == '__main__':
    run()
