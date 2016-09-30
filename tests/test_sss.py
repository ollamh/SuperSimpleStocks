import json
import datetime
from decimal import Decimal
import random
import unittest

from sss import GBCE, Stock


class StockTest(unittest.TestCase):

    def setUp(self):
        with open('data/stocks.json', 'r') as f:
            self.data = json.loads(f.read())
        self.gbce = GBCE(self.data)
        self.common_stock = self.gbce.stocks['POP']
        self.preferred_stock = self.gbce.stocks['GIN']

    def test_empty_gbce(self):
        gbce = GBCE()
        self.assertEqual(len(gbce.stocks), 0)

    def test_initialization(self):
        self.assertEqual(
            self.gbce.stocks.keys(),
            {i['stock_symbol']: Stock(i) for i in self.data}.keys()
        )

    def test_add_stock_fail(self):
        with self.assertRaisesRegex(AssertionError, 'Such symbol exists'):
            self.gbce.add_stock('ALE', 'Common', 60, 23)

    def test_add_stock_ok(self):
        self.gbce.add_stock('NEW', 'Common', 60, 23)
        self.assertIn('NEW', self.gbce.stocks.keys())

    def test_get_stock_ok(self):
        stock = self.gbce.get_stock('ALE')
        self.assertEqual(stock, self.gbce.stocks['ALE'])

    def test_get_stock_fail(self):
        with self.assertRaisesRegex(
                AssertionError, 'Stock symbol should exist'):
            self.gbce.get_stock('EEE')

    def test_wrong_type_stock_initialization(self):
        with self.assertRaisesRegex(
                AssertionError,
                'Stock type should be only Preferred or Common'):
            self.gbce.add_stock('NOS', 'Wrong', 60, 23)

    def test_wrong_par_value_stock_initialization(self):
        with self.assertRaisesRegex(AssertionError, 'Par value should be > 0'):
            self.gbce.add_stock('NOS', 'Common', '-60', 23)

    def test_wrong_last_dividend_stock_initialization(self):
        with self.assertRaisesRegex(
                AssertionError, 'Last dividend should be >= 0'):
            self.gbce.add_stock('NOS', 'Common', 60, '-23')

    def test_wrong_fixed_dividend_stock_initialization(self):
        with self.assertRaisesRegex(
                AssertionError, 'Fixed dividend percentage between 0 and 1'):
            self.gbce.add_stock('NOS', 'Preferred', 60, 23, '343')

    def test_remove_stock_ok(self):
        self.assertEqual(len(self.gbce.stocks), 5)
        self.gbce.remove_stock('ALE')
        self.assertEqual(len(self.gbce.stocks), 4)
        self.assertNotIn('ALE', self.gbce.stocks)

    def test_remove_stock_fail(self):
        with self.assertRaisesRegex(
                AssertionError, 'Stock symbol should exist'):
            self.gbce.remove_stock('NO_STOCK')

    def test_calculate_dividend_yield(self):
        self.assertEqual(self.common_stock.get_dividend_yield(100), 0.08)
        self.assertEqual(self.preferred_stock.get_dividend_yield(200), 0.01)

    def test_calculate_dividend_yield_wrong_fail(self):
        with self.assertRaisesRegex(
                AssertionError, 'Fail to calculate - not of preferred type'):
            self.common_stock._get_preferred_dividend_yield(200)

    def test_calculate_dividend_yield_wrong_price(self):
        with self.assertRaisesRegex(
                ValueError, 'could not convert string to float'):
            self.common_stock.get_dividend_yield('fgfg')
        with self.assertRaisesRegex(
                AssertionError, 'Price should be > 0'):
            self.preferred_stock.get_dividend_yield(-100)

    def test_sell_stock_ok(self):
        now = datetime.datetime.now()
        self.gbce.sell('POP', 200, 500)
        self.assertEqual(len(self.common_stock._trades), 1)
        trade = self.common_stock._trades[0]
        self.assertEqual(trade.quantity, 500)
        self.assertEqual(trade.price, 200)
        self.assertEqual(trade.indicator, 'sell')
        # Checking this for time equality can have side effects,
        # so just make sure the datetime exists and at least have the same day
        self.assertEqual(
            trade.timestamp.strftime('%Y-%m-%d'),
            now.strftime('%Y-%m-%d')
        )
        self.assertEqual(self.common_stock, trade.stock)

    def test_pe_ratio_ok(self):
        ratio = self.common_stock.p_e_ratio(300)
        self.assertEqual(ratio, 37.5)

    def test_pe_ratio_fail(self):
        with self.assertRaisesRegex(AssertionError, 'Price should be > 0'):
            self.gbce.stocks['ALE'].p_e_ratio('-300')
        with self.assertRaisesRegex(ValueError,
                                    'could not convert string to float'):
            self.gbce.stocks['ALE'].p_e_ratio('-sdf')

    def test_vvs_price_ok(self):
        self.assertEqual(len(self.common_stock._trades), 0)
        res = self.common_stock.volume_weighted_stock_price()
        self.assertEqual(res, 0)

        self.gbce.buy(self.common_stock._stock_symbol, 20, 200)
        self.gbce.buy(self.common_stock._stock_symbol, 200, 200)
        self.gbce.buy(self.common_stock._stock_symbol, 150, 400)
        self.gbce.sell(self.common_stock._stock_symbol, 350, 300)

        self.assertEqual(len(self.common_stock._trades), 4)

        res = self.common_stock.volume_weighted_stock_price()
        self.assertEqual(res, 190)

    def test_get_all_share_index(self):
        res = self.gbce.get_all_share_index()
        # we don't have any data
        self.assertEqual(res, 0)
        with open('data/trades.json', 'r') as f:
            self.trades = json.loads(f.read())
        for trade in self.trades:
            getattr(self.gbce, trade['indicator'])(
                trade['stock_symbol'], trade['price'], trade['quantity'])

        res = self.gbce.get_all_share_index()
        # Rounding up to 6th digit after point
        self.assertEqual(round(res, 6),  round(Decimal(275.849036), 6))

    def generate_trades(self):
        # Helper method for generating data (200 trades)
        random.seed()
        for i in range(0, 200):
            stock_symbol = random.choice(list(self.gbce.stocks.keys()))
            indicator = random.choice(['buy', 'sell'])
            price = round(random.random() * random.randint(10, 1000), 2)
            quantity = random.randint(10, 10000)
            getattr(self.gbce, indicator)(stock_symbol, price, quantity)


if __name__ == '__main__':
    unittest.main()
