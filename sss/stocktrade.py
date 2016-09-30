import datetime


class StockTrade:
    """
    Class for storing trade information
    - quantity
    - price
    - indicator, i.e. "buy" or "sell"
    - stock
    """

    def __init__(self, stock, price, quantity, indicator):
        assert float(price) > 0, 'Price should be > 0'
        assert indicator in ['buy', 'sell'], \
            'Indicator valid choices are buy and sell'
        assert int(quantity) > 0, 'Quantity should be integer and > 0'

        self._stock = stock
        self._price = float(price)
        self._indicator = indicator
        self._quantity = int(quantity)
        self._datetime = datetime.datetime.now()

    @property
    def price(self):
        return self._price

    @property
    def indicator(self):
        return self._indicator

    @property
    def quantity(self):
        return self._quantity

    @property
    def timestamp(self):
        return self._datetime

    @property
    def stock(self):
        return self._stock
