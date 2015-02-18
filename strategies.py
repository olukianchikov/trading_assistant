import sys
import os
from skeleton import *
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import kalman as ka


class BasicMR(Strategy):
    """Mean Reversion Strategy for one security with Bollinger Bands."""

    def __init__(self, security, lookback=30):
        self.__securities = []
        self.__securities = security   # it could be either one security or a list of security objects
        self.__positions = self.generate_positions()

    def test_stationary(self, lb=30):
        """ Method checks the stationarity of the price series.
        Works on internal list of securities.
        Returns: True/False if there is only one security, and a list of True/False if there are many securities.
           (True - stationary; False - non-stationary)
            ADF test is used.
        Parameter: lb => look-back period (in days). Default is 30 days.
            (Note also that the order of the results (indexes) are the same as the indexes for the list of
            securities contained in the current class object. It's a hint for you to know how to find security names for
            True results)."""
        if not isinstance(self.__securities, list):
            securities = [self.__securities]
        else:
            securities = self.__securities
        prices = [one_stock.get_prices(lb) for one_stock in securities]  # list comprehension
        results = [ts.adfuller(price_series, regression="c", autolag='AIC') for price_series in prices]
        simple_results = [BasicMR.simplify_adf_results(result[1], result[0], result[4]) for result in results]
        if len(simple_results) == 1:
            return simple_results[0]
        else:
            return simple_results


    @classmethod
    def simplify_adf_results(cls, p_value, test_statistic, crit_value):
        """Accepts the values p-value, test-statistic and crit-value as float parameters.
        Returns: True if the results show stationarity, False of not."""
        if p_value >= 0.05:
            return False
        else:
            if test_statistic >= crit_value:
                return False
            else:
                return True

    def replace_securities(self, security):
        """Accepts a security that replaces current security for which this Mean Reversion strategy makes analysis.
        They can be accepted as list too."""
        self.__securities = security

    def get_securities_names(self):
        """Returns the stored security's name.
        If there are many securities (in a list), returns a list of names."""
        if not isinstance(self.__securities, list):
            return self.__securities.get_name()
        else:
            return [one_security.get_name() for one_security in self.__securities]

    #@classmethod
    #def moving_average(cls, data_series, window):
    #    """Moving average of 'data_series' with window size 'window'."""
    #    output = np.empty(len(data_series) - window + x)
    #    for i in range(len(output)):
    #        output[i] = np.sum(data_series[i:i + window]) / window
    #    return output

    @classmethod
    def sma(cls, price_series, window):
        """Accepts price_series as Series and window in days as integer.
        Returns the Series object with moving average values."""
        weights = np.repeat(1.0, window)/window
        s_ma = np.convolve(price_series, weights, 'valid')
        return s_ma

    @classmethod
    def kalman_average(cls, price_series):
        """Invoking kalman algorithm that builds improved version of moving average.
        It accepts Series object with the price series.
        It returns Series of averages for the period."""
        obs = np.array([price_series.values])
        steps = len(price_series)
        result = ka.kalman(obs, nsteps=steps)
        result = pd.Series(result)
        return result

    @classmethod
    def bollinger_bands(cls, dates, prices, mov_avg, time_frame=20, z_threshold=1.67):
        """Accepts the moving average Series object and returns a list of two Series:
        upper band, and lower band threshold values."""
        sd = []
        sd_date = []
        i = time_frame
        while i <= len(prices):
            prices_in_frame = prices[i-time_frame:i]
            standev = prices_in_frame.std()
            sd.append(standev)
            sd_date.append(dates[i])
            i+=1
        #[sd_date, sd]
        top_band = [sd_date, mov_avg+(sd*z_threshold)]
        low_band = [sd_date, mov_avg-(sd*z_threshold)]
        return top_band, low_band

    @classmethod
    def get_slope(cls, price_series):
        """Is intended to be used with price series of the length of 40-100. Tells the slope. The bigger the value
        above 0, the stronger is the upward trend, thus entering only long positions makes more sense.
        The lower the returned value below 0, the stronger is the downward trend, thus it makes sense to enter
        only short positions. It assumes daily prices.
        Returns float type of slope."""
        slope = (price_series[-1] - price_series[0]) / len(price_series)
        return slope

    def generate_positions(self, long_only=False, time_frame=20, max_holding_period = 20):
        """Method builds best combination of positions that you can access with get_positions.
        Returns True if they were generated and False if there is no way they can be generated (no stationarity) or
        on error.
        Time Frame parameter sets look back period for stationarity check and bollinger bands. Default is 20."""
        result = []
        names = []
        if isinstance(self.__securities, list):
            securities_list = self.__securities
        else:
            securities_list = [ self.__securities ]
        stationarity_checked_securities = self.test_stationary(time_frame)
        index = 0
        for stat_result in stationarity_checked_securities:
            if stat_result == 0:
                names.append(securities_list[index].get_name())
                result.append(0)
                continue
            this_slope = BasicMR.get_slope(securities_list[index].get_prices(time_frame*4))  # longer-term slope check
            half_life = BasicMR.get_half_life(securities_list[index].get_prices())
            if (half_life is False) or (half_life > max_holding_period):
                names.append(securities_list[index].get_name())
                result.append(0)
                continue
            # Here we have only good candidates
            mov_avg = BasicMR.kalman_average(securities_list[index].get_prices())
            top_band, low_band = BasicMR.bollinger_bands(securities_list[index].get_history(time_frame*2+2)['Date'],\
                                                 securities_list[index].get_prices(time_frame*2+2), mov_avg,\
                                                 time_frame, 1.67)
            if this_slope > 0.4 and securities_list[index].get_prices()[-1] < low_band[-1]:  # Careful here - no dates check!
                names.append(securities_list[index].get_name())
                result.append(1)
            elif this_slope < -0.4 and securities_list[index].get_prices()[-1] > top_band[-1]:
                names.append(securities_list[index].get_name())
                result.append(-1)
            else:
                names.append(securities_list[index].get_name())
                result.append(0)
            index += 1
        return [names, result]

    @classmethod
    def get_half_life(cls, price_series):
        """The method accepts price series. It returns the half-life period in days. It returns False if lambda is
        positive or zero  (0 naturally means that the half-life period is super long)."""
        lagged_price = price_series.shift(1).fillna(method="bfill")
        delta = price_series - lagged_price
        beta = np.polyfit(lagged_price, delta, 1)[0]
        half_life = (-1*np.log(2)/beta)
        if beta >= 0:
            return False
        else:
            return half_life

    #def get_hurst(self, lag_range=30):
        # Doesn't work properly because sqrt of std makes no sense.
     #   """Calculates Hurst exponent for the current security's price series.
      #  If the result is < 0.5 => Mean-Reversion;
      #  0.5 => random walk;
      #  > 0.5 => a trend"""
      #  p = self.__securities.get_prices()
      #  tau = []
      #  lagvec = []
      #  #  Step through the different lags
      #  for lag in range(2, lag_range):
      #      #  produce price difference with lag
      #      pp = np.subtract(p[lag:], p[:-lag])
      #      #  Write the different lags into a vector
      #      lagvec.append(lag)
      #      #  Calculate the variance of the differnce vector
      #      tau.append(np.sqrt(np.std(pp)))
      #  #  linear fit to double-log graph (gives power)
      #  m = np.polyfit(np.log10(lagvec), np.log10(tau), 1)
      #  # calculate hurst
      #  hurst = m[0]*2
      #  return hurst

    def get_positions(self):
        """Returns a list of positions that have been generated a while ago (not now)."""
        return self.__positions