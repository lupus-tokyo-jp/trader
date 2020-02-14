# encode=UTF-8
import logging
import pprint
import json

import coincheck.market

class CoinCheckAPI:
    def __init__(self):
        self.market = coincheck.market.Market()

    # Public API
    def getTicker(self):
        value = self.market.ticker.all()
        print(json.dumps(value))

    # Public API
    def getTrade(self):
        value = self.market.trade.all()
        print(json.dumps(value))

    # Public API
    def getOrderbook(self):
        value = self.market.order_book.all()
        print(json.dumps(value))
