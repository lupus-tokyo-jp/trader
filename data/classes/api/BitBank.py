# encode=UTF-8
import logging
import pprint
import pprint
import json
import requests
import time
import hashlib
import hmac
import urllib

import env

class BitBankAPI:
    def __init__(self):
        # Load env.
        environment = env.environment()
        self.config = environment.config()

        self.pub_endpoint = 'https://public.bitbank.cc/'
        self.pri_endpoint = 'https://api.bitbank.cc/v1/'
        self.pair = environment.pair

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
        return obj

    def postSell(self):
        endpoint = 'user/spot/order'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'price': 30000,
            'amount': 10,
            'side': "sell",
            'pair': self.pair,
            'type': 'limit'
        }

        self.setRequestHeader(url, params)

        result = requests.post(url, data = json.dumps(params), headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def postBuy(self):
        endpoint = 'user/spot/order'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'price': 30000,
            'amount': 10,
            'side': "buy",
            'pair': self.pair,
            'type': 'limit'
        }

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

        print('> SET REQUEST HEADERS : BitBank > ' + json.dumps(self.requet_header))
        logging.info('> SET REQUEST HEADERS : BitBank > ' + json.dumps(self.requet_header))
