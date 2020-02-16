# encode=UTF-8
import logging
import pprint
import json

import python_bitbankcc

class BitBankAPI:
    def __init__(self):
        self.pub = python_bitbankcc.public()

    # Public API
    def getTicker(self):
        value = self.pub.get_ticker(
            'btc_jpy' # ペア
        )
        print(json.dumps(value))

    # Public API
    def getDepth(self):
        value = self.pub.get_depth(
            'btc_jpy' # ペア
        )
        # print(json.dumps(value))
        return value

    # Public API
    def getTransactions(self):
        value = self.pub.get_transactions(
            'btc_jpy' # ペア
            # '20170313' # YYYYMMDD 型の日付
        )
        print(json.dumps(value))

    # Public API
    def getCandlestick(self):
        value = self.pub.get_candlestick(
            'btc_jpy', # ペア
            '1hour', # タイプ
            '20170313' # YYYYMMDD 型の日付
        )
        print(json.dumps(value))