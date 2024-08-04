from data_classes import *

def run():
    bns = Stock('BNS','TSE')
    google = Stock('GOOGL', 'NASDAQ')
    shop = Stock('SHOP','TSE')
    msft = Stock('MSFT','NASDAQ')

    portfolio = Portfolio([Position(bns,100), Position(google,30), Position(shop,10), Position(msft,2)])
    print(portfolio.get_total_value())


if __name__ == '__main__':
    run()
