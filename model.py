__author__ = 'Lukianchikov'
import datahandler as dh
import sys
import os
import pandas as pd
import datetime
import strategies as st
import securities as sc
from matplotlib.finance import fetch_historical_yahoo
from matplotlib.finance import parse_yahoo_historical_ochl
import numpy as np
import datetime

class Model:

    def __init__(self):
        self.parser = None
        self.strategies = ['Mean Reversion with Bollinger Bands', 'Mean Reversion with Bollinger Bands: Long Only',
            'Mean Reversion with Bollinger Bands and two enty levels',
                           'Mean Reversion with Bollinger Bands and two entry levels: Long Only',
                           'Pair Trading', 'Index Arbitrage',
                            'Cointegration']
        self.descriptions = ['It\'s one stock strategy in a way that it tries to find mean reversion in each of specified'
                             'stocks, then it gives you recommendations how to trade them. It uses Bollinger Bands'
                             'with Kalman filter applied to moving average. If you want to find a combination'
                             'of stocks that mean reverts, then you should choose Cointegration.',
                             'It\'s one stock strategy that tries to find mean reversion in each of specified'
                             'stocks, and then it gives you recommendations how to trade them. It uses Bollinger Bands'
                             'with Kalman filter applied to moving average. This strategy assumes you cannot go short.'
                             'If you want to find a combination'
                             'of stocks that mean reverts, then you should choose Cointegration.',
                             'It\'s one stock strategy in a way that it tries to find mean reversion in each of specified'
                             'stocks, then it gives you recommendations how to trade them. It uses Bollinger Bands'
                             'with Kalman filter applied to moving average. It uses two entry levels - you buy one'
                             'unit of the stock in at first entry point, and another one at the second. '
                             'If you want to find a combination'
                             'of stocks that mean reverts, then you should choose Cointegration.',
                             'It\'s one stock strategy in a way that it tries to find mean reversion in each of specified'
                             'stocks, then it gives you recommendations how to trade them. It uses Bollinger Bands'
                             'with Kalman filter applied to moving average. It uses two entry levels - you buy one'
                             'unit of the stock in at first entry point, and another one at the second. You cannot go short. '
                             'If you want to find a combination'
                             'of stocks that mean reverts, then you should choose Cointegration.',
                             'This strategy is mean-reversion based, and tries to find a pair of stocks which price differenc is'
                             'mean reverting. It is in fact a cointegration strategy, but it\'s rather a particular case,'
                             'because you are limited to a pair of stocks. If you want to implement the same strategy but'
                             'for more than two stocks, choose Cointegration.',
                             'A strategy that tries to find arbitrage opportunities in the index and constituiting stocks.'
                             'You combine some stocks from the index (not all of them), and see whether the prices of this batch'
                             'and the index are cointegrating.',
                             'In this strategy you will obtain the weights of stocks (both short and long) that lead to '
                             'the price of this combination of stocks to mean revert.']

    def handleXlsx(self, filename, directory, progressNotifierFunction=None):
        self.parser = dh.XlsxParser()
        # This will take a while:
        self.parser.parse_excel(filename, directory, progressNotifierFunction)
        self.parser = None   # after completion - delete reference to the object

    @classmethod
    def fetchStockData(cls, beg, end, ffile, yahoo=True, ticker="AAPL"):
        """Depending on the boolean parameter yahoo, it will fetch the stock data from yahoo finance,
        or from the file, given that the file contains date columns and price columns where ticker name is the
        header for prices for that security."""
        if yahoo is True:
            p = fetch_historical_yahoo(ticker, beg, end)
            result = parse_yahoo_historical_ochl(p, False, True)
            return result
        else:
            result = os.path.exists(ffile)
            if result is False:
                raise FileNotFoundError("Error: {} file was not found.".format(ffile))
            f = pd.read_csv(ffile)
            max = len(f.columns)
            for i in range(1, max):
                cur_name = f.columns.values[i]
                if cur_name == ticker:
                    break
            prices = f.values[:, i]  # f.values and f.iloc have actual data starting from 0 index. First is row.
            max_rows = len(f.values[:, 0])
            """date, year, month, day, d, open, close, high, low, volume, adjusted_close"""
            results = []
            for j in range(0, max_rows):
                dt = datetime.date(*[int(val) for val in f.values[j, 0].split('-')])
                results.append((dt, 0, 0, 0,
                            0, 0, float(prices[j]), 0, 0, 0, float(prices[j])))
            my_type = np.dtype(
                [(str('date'), object),
                (str('year'), np.int16),
                (str('month'), np.int8),
                (str('day'), np.int8),
                (str('d'), np.float),
                (str('open'), np.float),
                (str('close'), np.float),
                (str('high'), np.float),
                (str('low'), np.float),
                (str('volume'), np.float),
                (str('aclose'), np.float)])
            d = np.array(results, dtype=my_type)
            return d.view(np.recarray)
        return result

    def get_strategies(self):
        return self.strategies

    def get_strategy_descriptions(self):
        return self.descriptions

    def load_names_from_csv(self, ffile):
        """Loads the asset names from a given csv"""
        names = []
        result = os.path.exists(ffile)
        if result is False:
            return ['Csv file not found.']
        f = pd.read_csv(ffile)
        max = len(f.columns)
        for i in range(1, max):
            name = f.columns.values[i]
            names.append(name)
        return names

    def load_first_date_from_csv(self, ffile):
        result = os.path.exists(ffile)
        if result is False:
            raise Exception("No csv-file found. Can't get first date!")
        f = pd.read_csv(ffile)
        last_date = f.iloc[1, 0]
        return datetime.datetime.strptime(last_date, '%Y-%m-%d').date()

    def load_last_date_from_csv(self, ffile):
        result = os.path.exists(ffile)
        if result is False:
            raise Exception("No csv-file found. Can't get first date!")
        f = pd.read_csv(ffile)
        last_date = f.iloc[-1, 0]
        return datetime.datetime.strptime(last_date, '%Y-%m-%d').date()

    def create_strategy(self, int_strategy, list_sec_names, hfile):
        list_sec = []
        for sec in list_sec_names:
            list_sec.append(sc.Stock(sec, hfile))
        if int_strategy is 0:
            mr_strategy = st.BasicMR(list_sec)
        return mr_strategy.get_positions()
