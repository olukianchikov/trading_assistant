import sys
import os
from skeleton import *
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
import kalman as ka
import johansen as jn
import datetime


class BasicMR(Strategy):
    """Mean Reversion Strategy for one security with Bollinger Bands.
    If many securities supplied, it analyzes Mean Reversion for every single stock."""

    def __init__(self, security, beg_date,  end_date, max_hold_period=40):
        self._securities = []
        self._securities = security   # it could be either one security or a list of security objects
        self.__positions = self.generate_positions(False, beg_date, end_date, max_hold_period)

    def test_stationary(self, securities_list, beg_date, end_date):
        """ Method checks the stationarity of the price series.
        Works on internal list of securities.
        Returns: True/False if there is only one security, and a list of True/False if there are many securities.
           (True - stationary; False - non-stationary)
            ADF test is used.
        Parameter: lb => look-back period (in days). Default is 30 days.
            (Note also that the order of the results (indexes) are the same as the indexes for the list of
            securities contained in the current class object. It's a hint for you to know how to find security names for
            True results)."""
        if not isinstance(securities_list, list):
            securities = [securities_list]
        else:
            securities = securities_list
        prices = []
        for j in range(0, len(securities)):
            tmp = securities[j].get_prices(beg_date, end_date)
            prices.append(tmp)
        results = []
        for price_series in prices:
            print(price_series)
            tmp = ts.adfuller(price_series, regression="c", autolag='AIC')
            results.append(tmp)
        simple_results = [BasicMR.simplify_adf_results(result[1], result[0], float(result[4]['5%'])) for result in results]
        if len(simple_results) == 1:
            return simple_results
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
        self._securities = security

    def get_securities_names(self):
        """Returns the stored security's name.
        If there are many securities (in a list), returns a list of names."""
        if not isinstance(self._securities, list):
            return self._securities.get_name()
        else:
            return [one_security.get_name() for one_security in self._securities]

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
        """"""
        slope = ((price_series[len(price_series)-1]/price_series[0]) - 1) / len(price_series)
        return slope

    def generate_positions(self, long_only, beg_date, end_date=datetime.date.today(), max_holding_period = 20):
        """Method builds best combination of positions that you can access with get_positions.
        Returns True if they were generated and False if there is no way they can be generated (no stationarity) or
        on error.
        Time Frame parameter sets look back period for stationarity check and bollinger bands. Default is 20."""
        result = []
        names = []
        if isinstance(self._securities, list):
            securities_list = self._securities
        else:
            securities_list = [ self._securities ]
        stationarity_checked_securities = []
        stationarity_checked_securities = self.test_stationary(securities_list, beg_date, end_date)
        index = 0
        for stat_result in stationarity_checked_securities:
            if stat_result == 0:
                names.append(securities_list[index].get_name())
                result.append(0)
                index += 1
                continue
            day_delta = end_date - beg_date
            day_delta = day_delta.days
            if day_delta > 20:
                window = 80    # 4 month slope
            else:
                window = 40
            beginning_of_slope = end_date - datetime.timedelta(days=window)
            this_slope = BasicMR.get_slope(securities_list[index].get_prices(beginning_of_slope, end_date))  # longer-term slope check
            half_life = BasicMR.get_half_life(securities_list[index].get_prices(beg_date, end_date))
            if (half_life is False) or (half_life > max_holding_period):
                # The half-life is too big.
                names.append(securities_list[index].get_name())
                result.append(0)
                index += 1
                continue
            # Here we have only good candidates
            mov_avg = BasicMR.kalman_average(securities_list[index].get_prices())

            boll_window = 20  #  <--- THIS COULD BE CHOSEN BY USER
            beg_boll = end_date - datetime.timedelta(days=boll_window)
            top_band, low_band = BasicMR.bollinger_bands(securities_list[index].get_history(beg_boll, end_date)['Date'],\
                                                 securities_list[index].get_prices(beg_boll, end_date), mov_avg,\
                                                 boll_window, 1.67)
            one_day_back = end_date - datetime.timedelta(days=1)
            if this_slope > 0.0025 and securities_list[index].get_prices(one_day_back, end_date)[-1] < low_band[-1]:  # Careful here - no dates check!
                names.append(securities_list[index].get_name())
                result.append(1)
            elif this_slope < -0.0025 and securities_list[index].get_prices(one_day_back, end_date)[-1] > top_band[-1]:   # Left here.......
                names.append(securities_list[index].get_name())
                if long_only is False:
                    result.append(-1)
                else:
                    result.append(0)  # We give no recommendation when see short selling signal if long only set to True
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
      #  p = self._securities.get_prices()
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

class LongBasicMR(BasicMR):
    """The same thing as Basic Mean reversion class, but for simplicity, the instances of this class will be
    long only strategies."""
    def __init__(self, security, beg_date,  end_date, max_hold_period=40):
        super(LongBasicMR, self).__init__(security, beg_date,  end_date, max_hold_period)

    def generate_positions(self, long_only=True, time_frame=20, max_holding_period=40):
        print("Children's Method Called! Yey!")
        long_only = True
        return BasicMR.generate_positions(self, beg_date,  end_date, max_hold_period)

class Cointegration(BasicMR):
    """ Class that implements trading strategy based on Johansen test of cointegration."""

    def __init__(self, security, beg_date,  end_date, max_hold_period=40):
        super(Cointegration, self).__init__(security, beg_date,  end_date, max_hold_period)

    def generate_positions(self, long_only, beg_date, end_date=datetime.date.today(), max_holding_period=20):
        """Method builds best combination of positions that you can access with get_positions.
        Returns True if they were generated and False if there is no way they can be generated (no stationarity) or
        on error.
        Time Frame parameter sets look back period for stationarity check and bollinger bands. Default is 20."""
        result = []
        names = []
        securities_list= []
        if isinstance(self._securities, list):
            securities_list = self._securities
        else:
            raise Exception("Error: for cointegration strategy you have to choose more than one security.")
        #generate the matrix of price series:
        prices = []
        # CHECK ALL THE DATES OF PRICES ARE THE SAME:
        for i in range(0, len(securities_list)):
            tmp = securities_list[i]
            print("I:{}".format(i))
            prices.append([ tmp.get_dates(beg_date, end_date), tmp.get_prices(beg_date, end_date)])
        print(prices[0]) #<<<<<<<<<<<<<<<<<<<<<<<<<<
        shortest_dates_length = len(prices[0][0])
        shortest_dates_index = 0
        max = len(prices)
        for i in range(1, max):
            tmp_length = len(prices[i][0])
            if tmp_length < shortest_dates_length:
                shortest_dates_length = tmp_length
                shortest_dates_index = i
        df = pd.DataFrame({"dates": prices[shortest_dates_index][0], securities_list[shortest_dates_index].get_name(): prices[shortest_dates_index][1]})
        print("::::::::::::::::::::::::::::::")
        print(df)
        for i in range(0, len(securities_list)):
            print("current i is {}".format(i))
            print("Name is {}".format(securities_list[i].get_name()))
            if i == shortest_dates_index:
                continue
            df_new = pd.DataFrame({"dates": prices[i][0], securities_list[i].get_name(): prices[i][1]})
            df = df.merge(df_new, on='dates', how="inner")
        # NOW df should contain only dates and prices for the shortest period of dates among all the securities...
        print("..................................................")
        print(df)
        # MAYBE RETURN THE BEGINNIG OF ANALYZED PERIOD AND END?
        extra_output = []
        extra_output.append("The beginning of the analyzed period is {}".format(df['dates'].irow(0)))
        extra_output.append("The end of the analyzed period is {}".format(df['dates'].irow(-1)))
        df = df.drop("dates", axis = 1)
        price_matrix = df.as_matrix()
        print(price_matrix.shape)
        print("Price matrix is this:")
        print(price_matrix)
        res = jn.coint_johansen(price_matrix, 0, 1)
        """ esult.eig  = eigenvalues  (m x 1)
%          result.evec = eigenvectors (m x m), where first
%                        r columns are normalized coint vectors
%          result.lr1  = likelihood ratio trace statistic for r=0 to m-1
%                        (m x 1) vector where r is the number of cointegrating combinations, m is the
                         total number of variables. Remember, if r=m, then all the variables are stationary by
                         themselves and we do not need cointegration anymore.
%          result.lr2  = maximum eigenvalue statistic for r=0 to m-1
%                        (m x 1) vector.
%          result.cvt  = critical values for trace statistic
%                        (m x 3) vector [90% 95% 99%]
                         So each row is given for each test (r=0, r=1, r=2..., r=m-1). And then there are 3 columns for 90, 95 and 99
%          result.cvm  = critical values for max eigen value statistic
%                        (m x 3) vector [90% 95% 99%]
%          result.ind  = index of co-integrating variables ordered by
%                        size of the eigenvalues from large to small"""
        print("trace statistic: \n{}".format(res.lr1))
        print("trace statistic crit values: \n{}".format(res.cvt))
        print("Eigenvalue statistic: \n{}".format(res.lr2))
        print("Eigenvalue statistic crit values: \n{}".format(res.cvm))
        print("Eigenvalues: \n{}".format(res.eig))
        print("Eigen vectors: \n{}".format(res.evec))
        names = df.columns.values
        extra_output.append("\n")
        extra_output.append("Trace Value statistics:\n {}".format(res.lr1))
        extra_output.append("Trace Critical Values:\n {}".format(res.cvt))
        extra_output.append("\n")
        extra_output.append("Eigen Value statistics:\n {}".format(res.lr2))
        extra_output.append("Versus Critical Values:\n {}".format(res.cvm))
        extra_output.append("\n")
        # Check how many cointegrating combinations there are:
        num_combinations = 0
        weights = []
        for i in range(0, len(res.lr1)):
            print(res.lr1[i])
            print(res.cvt[i, 1])
            print("_____")
            if res.lr1[i] < res.cvt[i, 1]:    # HAVE TO CHECK WHETHER 1 here is really refer to a column index...
                num_combinations = i
                break
        if num_combinations == 0:
            for j in range(0, len(names)):
                weights.append(0)
            result = [names, weights, extra_output]   # ALSO RETURN TEXT THAT NO COMBINATIONS FOUND??
        else:
            #FIND HIGHEST EIGENVALUE AND RETURNS ITS CORRESPONDING COLUMN IN EIGEN VECTORS
            best_index = 0
            for i in range(1, len(res.lr2)):
                if res.lr2[i] > res.cvm[i, 1]:
                    if res.lr2[i] > res.lr2[best_index]:
                        best_index = i
            for j in range(0, len(names)):
                weights.append(res.evec[j, best_index])
            # express weights in relation to first security:
            divisor = weights[0]
            for j in range(0, len(weights)):
                weights[j] = weights[j] / divisor
            #For the half life analysis, I need:
            price_series = pd.Series()
            max = len(price_matrix[:, 0])
            for i in range(0, max):
                agg_price = 0
                for k in range(0, len(price_matrix[i, :])):
                    agg_price = agg_price + price_matrix[i, k] * weights[k]  # Aggregate price of given weights
                price_series.set_value(i, agg_price)
            half_life = BasicMR.get_half_life(price_series)
            extra_output.append("Half life period: {}".format(half_life))
            result = [names, weights, extra_output]
        # For further backtesting, add weights and half life to the properties of this object....
        return result



