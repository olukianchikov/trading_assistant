#from yahoo_finance import Share   Only for Python 2.xx
import sys
import os
from skeleton import *
import traceback
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
from datetime import datetime as dt


class WrongHistoryFileError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(WrongHistoryFileError, self).__init__(message)


class Stock(Security):
    """Class representing stock. Main operations are made around stored pairs of date and price."""
    def __init__(self, name, history_file=None):
        self.__name = name
        self.__history = None
        self.__date = None
        self.__price = None
        self.__history_file = None
        try:
            if history_file is "":
                history_file = None
            if history_file is not None:
                if Stock.check_file(history_file):
                    self.__history_file = history_file
                    self.fill_history(history_file)
                else:
                    self.__history = None
                    self.__history_file= None
            else:
                self.fill_history()
                self.__history_file = None
        except WrongHistoryFileError as e:
                sys.stderr.write('ERROR: %s\n' % str(e))

    @classmethod
    def check_file(cls, history_file):
        """Returns True if the file exists and False if it doesn't."""
        result = os.path.exists(history_file)
        return result

    def fill_history(self, hfile=None):
        """Method sets the history of prices from history csv-file provided at the creation
        or here in the method. If no file ever been provided, then Yahoo finance is used to
        retrieve historical data. IT stores the history as a DataFrame type internally as a
        parameter for the instance.
        It also updates last date and price in the object.
        See getCurrentPrice() and getCurrentDate() to retrieve those values.
        If history file is used, the method will try to make prices up to date by querying Yahoo Finance. However,
        it is possible for Yahoo Finance not to have the data on that stock, thus the update wouldn't be successful.
        If a file with multiple securities passed, the method will take the dates and the prices columns where the price
        must have the column name exactly the same as security's name."""
        if hfile is not None:
            if os.path.isfile(hfile):
                f = pd.read_csv(hfile)
            else:
                raise FileNotFoundError("The file supplemented can't be found.")
        else:
            if self.__history_file is not None:
                # analyze the history file and load prices
                f = pd.read_csv(self.__history_file)
                # Check with current date that the last record is the last:
                f = Stock.finalize_history(f)
                #     <- That upper one will return the same f if it's indeed updated/relevant history.
                #     Will fill up the remaining part and return complete f otherwise.
            else:
                # load prices from yahoo
                f = Stock.fetch_yahoo(self.__name)
                if f is False:
                    raise ValueError("Error: cannot retrieve the data from Yahoo Finance for {}.".format(self.__name))
        self.__history = pd.DataFrame(f.iloc[0:, 0], columns=['Date'])  # loaded history it is a list of date
        # and price
        self.__history[self.__name] = f[self.__name]
        self.__date = f.iloc[-1,0]
        self.__price = f[self.__name].iloc[-1]
        return True

    @classmethod
    def fetch_yahoo(cls, name):
        """Returns a data frame with dates and prices for a given security name.
        The latest dates at the end of the data frame."""
        url_string = "http://chart.yahoo.com/table.csv?s="
        #url_string = "http://finance.google.com/finance/info?client=ig&q="
        url_string = url_string + name
        try:
            f = pd.read_csv(url_string)
            f = f[::-1]  # reversing, so that the last row is the newest value.
            f = f.rename(columns={'Close':name})
            return f
        except Exception as e:
            sys.stderr.write(str(e))
            return False

    def get_current_price(self):
        """Returns the price (float) of the last stored date."""
        return self.__price

    def get_current_date(self):
        """Returns the last stored date. Type: String."""
        return self.__date

    #def set_history(self,history_file,func_find_last_date):
    #    self.history=history_file
    #    def history_last_date_wrapper():
    #        return func_find_last_date(history_file)
    #    self.history_end=history_last_date_wrapper

    def update(self, history_file=None):
        """Updating the history of prices up until last available price.
        You can then use get_current_price and get_current_date to see the last ones.
        Returns false if update fails.
        If you supplement the history file, then it updates the prices from it AND from Yahoo Finance if
        they have newer dates. Otherwise, without arguments it appends Yahoo Finance Prices to existing ones (stored
        in the object), or does the addition exclusive with Yahoo Finance prices."""
        if history_file is not None:
            return self.fill_history(self, history_file)
        else:
            return self.fill_history(self)

    def get_history(self, beg, end):
        """Returns the data frame of dates and prices."""
        try:
            if isinstance(self.__history, pd.core.frame.DataFrame):
                return self.__history[:][(self.__history["Date"] >= beg) & (self.__history["Date"] <= end)]
            else:
                raise Exception("The history data frame does not exist internally in this instance.")
        except Exception as e:
            sys.stderr.write(str(e))

    def finalize_history(self, df):
        """Class Method that accepts the data frame object with the dates and prices as its columns.
        It checks with today's date whether the last row is the latest one. If not, then it connects to Yahoo
        in order to append the last price data to the data frame. Returns the data frame, which will be updated
        data frame or the same one depending on whether the last record is the latest possible or not."""
        today = dt.today().date()
        last_day = df['Date'][-1]
        last_day = dt.strptime(last_day, '%Y-%m-%d')
        if last_day == today :
            return df
        else:
            try:
                df2 = Stock.fetch_yahoo(self.__name)
                k = None
                for index, row in df2.iterrows():
                    row_date = dt.stptime(row['Date'], '%Y-%m-%d')
                    if row_date == last_day:
                        k = index
                        break
                if k is not None:
                    mmax = len(df2.index)
                    for i in list(range(k, mmax)):
                        df.append(today, df2[i])
                else:
                    raise Exception("""Error: Cannot refill the data for the object because Yahoo Finance Data is much
                    newer.""")
                return df
            except Exception as e:
                sys.stderr.write(str(e))
                return df

    def get_name(self):
        """Returns a string containing of name of the stock of the object."""
        return self.__name

    def get_prices(self, beg, end):
        """Returns the series of prices. By default, returns the prices for the whole period stored in the instance.
        You can set a parameter which means prices of how many last days to return."""
        if isinstance(self.__history, pd.core.frame.DataFrame):
            prices = []
            for index, row in self.__history.iterrows():
                if (dt.strptime(self.__history["Date"][index], "%Y-%m-%d").date() >= beg)&\
                (dt.strptime(self.__history["Date"][index], "%Y-%m-%d").date() <= end):
                    prices.append(self.__history[self.__name][index])
            k = pd.Series(prices)
            return k

    def get_dates(self, beg, end):
        if isinstance(self.__history, pd.core.frame.DataFrame):
            dates = []
            for index, row in self.__history.iterrows():
                if (dt.strptime(self.__history["Date"][index], "%Y-%m-%d").date() >= beg)&\
                (dt.strptime(self.__history["Date"][index], "%Y-%m-%d").date() <= end):
                    dates.append(self.__history["Date"][index])
            k = pd.Series(dates)
            return k



class ETF(Stock):
    """ETF class is used to create ETF securities. Main focus is the pairs of date and price stored internally.
    At the moment, all the methods are the same as for the Stock class."""
    def __init__(self):
        Stock.__init__(self)
