from . import alpaca
from . import stock
from . import exchange
from . import portfolio

""" 
Simulator is in early ALPHA stages 

"""

class Simulator:
    def __init__():
        print(" Simulator is in ALPHA! ")
        self.equity = 100_000
        self.owned_stocks = {} # { Stock.name : [price, price] }
        self._time = 0
        self._historical_data = {} # { Stock.name : [price, price] }
        self.exchanges = [
            "NASDAQ",
            "NYSE",
            "ARCA",
            "BATS",
        ]

    @property
    def time(self):
        return self._time


    def run():
        """ turns on time and interaties over historical data """
        pass

    @property
    def historical_data(self):
        """ goes over all stocks and saves all the data """
        self._historical_data = []
        for stk in self.stocks:  
            self._historical_data{stk.symbol} = stk.historical_data()
        return self._historical_data   


    def buy(self, sym, qty):
        """ add a new stock to simulated portfolio """
        self.equity - qty*self.price(stk)
        self.owned_stocks[sym] += qty*[self.price(stk)]


    def sell(self, stk, qty):
        """ remove a new stock to simulated portfolio """
        self.equity + qty*self.price(stk)
        del self.owned_stocks[sym][-1*qty:]

    def price(self, sym):
        return self._historical_data[sym][0]
