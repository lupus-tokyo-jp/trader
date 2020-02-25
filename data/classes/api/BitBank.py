# encode=UTF-8
import sys
import pprint
import json
import requests
import time
import hashlib
import hmac
import urllib

import env
import classes.utility

class BitBankAPI:
    def __init__(self):
        self.cls_n = __class__.__name__

        # Load env.
        environment = env.environment()
        self.config = environment.config()

        # Set parameters
        self.pub_endpoint = 'https://public.bitbank.cc/'
        self.pri_endpoint = 'https://api.bitbank.cc/v1/'
        self.pair = environment.pair

        # Load utility.
        self.util = classes.utility.Utility()

        # request header.
        self.requet_header = {
            'content-type': 'application/json'
        }

    # Public API
    # sell	string	the lowest price of sell orders
    # buy	string	the highest price of buy orders
    # high	string	the highest price in last 24 hours
    # low	string	the lowest price in last 24 hours
    # last	string	the latest price executed
    # vol	string	trading volume in last 24 hours
    # timestamp	number	ticked at unix timestamp
    def getTicker(self):
        endpoint = 'ticker'
        url = str(self.pub_endpoint + self.pair + '/' + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    # Public API
    # asks 売り注文の情報
    # bids 買い注文の情報
    def getDepth(self):
        endpoint = 'depth'
        url = str(self.pub_endpoint + self.pair + '/' + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        obj = obj['data']
        del obj['timestamp']
        del obj['sequenceId']
        return obj

    def postSell(self, amount: int, price: int):
        endpoint = 'user/spot/order'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'price': price,
            'amount': amount,
            'side': "sell",
            'pair': self.pair,
            'type': 'limit'
        }
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'params > ' + json.dumps(params))

        self.setRequestHeader(url, params)

        result = requests.post(url, data = json.dumps(params), headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def postBuy(self, amount: int, price: int):
        endpoint = 'user/spot/order'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'price': price,
            'amount': amount,
            'side': "buy",
            'pair': self.pair,
            'type': 'limit'
        }
        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'params > ' + json.dumps(params))

        self.setRequestHeader(url, params)

        result = requests.post(url, data = json.dumps(params), headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def setRequestHeader(self, path: str, params = None):
        nonce = str(round(time.time() * 1000))
        message = nonce + json.dumps(params)

        signature = hmac.new(bytearray(self.config['private']['BitBank']['api_secret'], 'utf8'), bytearray(message, 'utf8'), hashlib.sha256).hexdigest()
        self.requet_header.setdefault('ACCESS-NONCE', nonce)
        self.requet_header.setdefault('ACCESS-KEY', self.config['private']['BitBank']['access_key'])
        self.requet_header.setdefault('ACCESS-SIGNATURE', signature)

        self.util.outputInfo(self.cls_n, sys._getframe().f_code.co_name, 'params > ' + json.dumps(params))
