from decimal import Decimal
from functools import reduce
from operator import mul

from .stock import Stock

__all__ = ['GBCE']


class GBCE:
    """
    Stands for Global Beverage Corporation Exchange
    Main class for operating exchange life cycle.
    Contains methods for adding, removing, buying, selling stocks
    and getting certain stock info
    """
    def __init__(self, stocks=None):
        """
        Initialization
        :param stocks: Non required, list of dictionaries,
        each containing structure like this
         {
           'fixed_dividend': None,
           'last_dividend': 23,
           'par_value': 60,
           'stock_symbol': 'ALE',
           'type': 'Common'
         }
        """
        self.stocks = {}
        if stocks:
            self.stocks = {i['stock_symbol']: Stock(i) for i in stocks}

    # Stock operations

    def add_stock(
            self, stock_symbol, type, par_value, last_dividend,
            fixed_dividend=None):
        """
        Creates stock
        :param stock_symbol: String stock symbol, e.g. 'POP'
        :param type: String choice of two stock types 'Common' and 'Preferred'
        :param par_value: Integer greater or equal zero (pennies)
        :param last_dividend: Integer greater or equal zero (pennies)
        :param fixed_dividend: Float or None, greater or equal zero
                               and less than 1 (percentage)
        """
        assert stock_symbol not in self.stocks, 'Such symbol exists'

        self.stocks[stock_symbol] = Stock({
            'stock_symbol': stock_symbol,
            'type': type,
            'par_value': par_value,
            'last_dividend': last_dividend,
            'fixed_dividend': fixed_dividend
        })

    def remove_stock(self, stock_symbol):
        """
        Removes stock from exchange
        :param stock_symbol: Stock symbol, e.g. 'POP'
        """
        assert stock_symbol in self.stocks, 'Stock symbol should exist'
        del self.stocks[stock_symbol]

    def get_stock(self, stock_symbol):
        """
        Returns stock object
        :param stock_symbol: String stock symbol, like 'ALE'
        :return: Stock object
        """
        assert stock_symbol in self.stocks, 'Stock symbol should exist'
        return self.stocks[stock_symbol]

    def buy(self, stock_symbol, price, quantity):
        """
        Buys certain stock
        :param stock_symbol: Stock symbol, e.g. 'POP'
        :param price: Float greater than zero
        :param quantity: Integer greater than zero
        """
        assert stock_symbol in self.stocks, 'Stock symbol should exist'
        self.stocks[stock_symbol].buy(price, quantity)

    def sell(self, stock_symbol, price, quantity):
        """
        Sells certain stock
        :param stock_symbol: Stock symbol, e.g. 'POP'
        :param price: Float greater than zero
        :param quantity: Integer greater than zero
        """
        assert stock_symbol in self.stocks, 'Stock symbol should exist'
        self.stocks[stock_symbol].sell(price, quantity)

    # Exchange information

    def get_all_share_index(self):
        """
        Get All Share Index as geometric mean of volume weighted stock prices
        :return: Float number
        """
        vvs_prices = []
        for stock_symbol, stock in self.stocks.items():
            vvs_prices.append(stock.volume_weighted_stock_price())
        return self.geometric_mean(vvs_prices)

    # Utilities

    @staticmethod
    def geometric_mean(p):
        """
        Calculates geometric mean
        :param p: List of floats
        :return: Nth root of multiplication of N floats
        """
        return Decimal(reduce(mul, p)) ** (Decimal(1.0) / Decimal(len(p)))
