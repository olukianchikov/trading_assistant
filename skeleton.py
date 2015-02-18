from abc import ABCMeta, abstractmethod

class Strategy(object):
    """Strategy is an abstract class providing the carcass for the child
    trading strategy classes. All the implemented trading strategy claseses
    must be derived from this class"""

    __metaclass__=ABCMeta

    @abstractmethod
    def generate_positions(self):
        """Method constructs a list of positions (weights) in all the stocks supplied to the
        object on creation. It is done in according to the strategy implemented."""
        raise NotImplementedError("You must implement generate_positions()!")

    @abstractmethod
    def get_positions(self):
        """This method returns a list of positions in accordance with particular strategy.
        It is needed for portfolio object."""
        raise NotImplementedError("You must implement get_positions()!")

class Portfolio(object):
    __metaclass__=ABCMeta
    """This is the abstract class for portfolios (i.e. trading positions)"""

    @abstractmethod
    def get_PLSeries(self):
        """It returns a list of dates and profilt loss account for last 30 days"""
        raise NotImplementedError("You forgot to implement getPLSeries() for your child class!")

    @abstractmethod
    def update(self):
        """this method updates all the risk metrics and profil/loss account."""
        raise NotImplementedError("You forgot to implement update() for your child class!")

    @abstractmethod
    def get_VAR(self):
        raise NotImplementedError("getVAR() not implemented!")

    @abstractmethod
    def rebuild_portfolio(self, strategy, *strategies):
        raise NotImplementedError("rebuildPortfolio() not implemented!")

    @abstractmethod
    def modify_positions(self, List_of_security_and_weight):
        raise NotImplementedError("modifyPositions() not implemented!")

    @abstractmethod
    def back_test(self):
         raise NotImplementedError("backTest() not implemented!")

class Security(object):
    __metaclass__=ABCMeta
    """This class is used to create securities such as stocks and ETFs (particular implementation can be implemented),"""

    @abstractmethod
    def update():
        """updating all the parameters such as last price, date"""
        raise NotImplementedError("update() not implemented!")

