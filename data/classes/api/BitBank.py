# encode=UTF-8
import logging
import pprint
import pprint
import json
import requests

import env

class BitBankAPI:
    def __init__(self):
        # Load env.
        environment = env.environment()
        self.config = environment.config()

        self.pub_endpoint = 'https://public.bitbank.cc/'
        self.pair = 'btc_jpy'

    # Public API
    # sell	string	the lowest price of sell orders
    # buy	string	the highest price of buy orders
    # high	string	the highest price in last 24 hours
    # low	string	the lowest price in last 24 hours
    # last	string	the latest price executed
    # vol	string	trading volume in last 24 hours
    # timestamp	number	ticked at unix timestamp
    def getTicker(self):
        endpoint = '/ticker'
        url = str(self.pub_endpoint + self.pair + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    # Public API
    # asks 売り注文の情報
    # bids 買い注文の情報
    def getDepth(self):
        endpoint = '/depth'
        url = str(self.pub_endpoint + self.pair + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    def postSell(self):
        msg = "BitBank sell"
        return msg

    def postBuy(self):
        msg = "BitBank buy"
        return msg
