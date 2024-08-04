from dataclasses import dataclass
import helpers as h

@dataclass
class Stock:
    ticker: str
    exchange: str
    price: float = 0
    currency: str = 'USD'
    usd_price: float = 0

    def __post_init__(self):
        price_info = h.get_price_information(self.ticker, self.exchange)
        
        if(price_info['ticker'] == self.ticker):
            self.price = price_info['price']
            self.currency = price_info['currency']
            self.usd_price = price_info['usd_price']

@dataclass
class Position:
    stock: Stock
    quantity: int


@dataclass
class Portfolio:
    positions: list[Position]

    def get_total_value(self):
        total_value = 0

        for position in self.positions:
            total_value += position.stock.usd_price * position.quantity

        return round(total_value,2)
