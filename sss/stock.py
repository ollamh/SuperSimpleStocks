import datetime
from dateutil import parser

import numpy as np

from .stocktrade import StockTrade

__all__ = ['Stock']


class Stock:
    """
    Basic stock class
    Encapsulates all methods regarding the stock life in GBCE.
    """
    def __init__(self, stock):
        """
        Initialization
        :param stock: Dictionary, containing structure like this:
        {
           'fixed_dividend': None,
           'last_dividend': 23,
           'par_value': 60,
           'stock_symbol': 'ALE',
           'type': 'Common'
         }
        :return:
        """
        fixed_dividend = stock.get('fixed_dividend')

        assert int(stock.get('par_value')) >= 0, 'Par value should be > 0'
        assert stock.get('type') in ['Common', 'Preferred'], \
            'Stock type should be only Preferred or Common'
        assert int(stock.get('last_dividend')) >= 0, \
            'Last dividend should be >= 0'
        if fixed_dividend:
            assert 0 <= float(fixed_dividend) <= 1, \
                'Fixed dividend percentage between 0 and 1'

        self._stock_symbol = stock.get('stock_symbol')
        self._type = stock.get('type')
        self._par_value = int(stock.get('par_value'))
        self._last_dividend = int(stock.get('last_dividend'))
        self._fixed_dividend = float(
            fixed_dividend) if fixed_dividend else None
        self._trades = []

    def is_preferred(self):
        """
        Checks if stock type is preferred.
        To check for common, just use if not stock.is_preferred()
        since there are only two options
        :return: Boolean
        """
        return self._type == 'Preferred'

    def get_dividend_yield(self, price):
        """
        Get dividend yield depending on stock type
        :param price: Float number
        :return: Float number
        """
        if self.is_preferred():
            return self._get_preferred_dividend_yield(price)
        else:
            return self._get_common_dividend_yield(price)

    def _get_preferred_dividend_yield(self, price):
        """
        Calculates preferred dividend yield
        :param price: Float number
        :return: Float number
        """
        assert self.is_preferred(), 'Fail to calculate - not of preferred type'
        assert float(price) > 0, 'Price should be > 0'
        return self._fixed_dividend * self._par_value / price

    def _get_common_dividend_yield(self, price):
        """
        Calculates common dividend yield
        :param price: Float number
        :return: Float number
        """
        assert float(price) > 0, 'Price should be > 0'
        return self._last_dividend / price

    def p_e_ratio(self, price):
        """
        Calculates p/e ratio
        :param price: Float
        :return:
        """
        assert float(price) > 0, 'Price should be > 0'
        return price / self._last_dividend if self._last_dividend > 0 else 0

    def volume_weighted_stock_price(self, last_5_minutes=True):
        """
        Returns weighted stock price based on prices and quantities
        :param last_5_minutes: By default uses only last 5 minutes trades
        :return: Float number
        """
        trades = self._trades
        if last_5_minutes:
            start = datetime.datetime.now() - datetime.timedelta(minutes=5)
            end = datetime.datetime.now()
            trades = self.get_trades(start, end)

        quantities = list(map(lambda x: x.quantity, trades))
        prices = list(map(lambda x: x.price, trades))
        prices = np.array(prices)
        quantities = np.array(quantities)
        sum_quantities = quantities.sum()
        return prices.dot(quantities)/sum_quantities if sum_quantities else 0

    def _trade(self, price, quantity, indicator):
        self._trades.append(StockTrade(self, price, quantity, indicator))

    def buy(self, price, quantity):
        self._trade(price, quantity, 'buy')

    def sell(self, price, quantity):
        self._trade(price, quantity, 'sell')

    def get_trades(self, start, end):
        if isinstance(start, str):
            start = parser.parse(start)
        if isinstance(end, str):
            end = parser.parse(end)
        assert start < end, 'Start datetime should be less than end one'
        return list(filter(
            lambda x: start <= x.timestamp <= end,
            self._trades
        ))
