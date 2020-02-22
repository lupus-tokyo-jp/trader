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

class CoinCheckAPI:
    def __init__(self):
        # Load env.
        environment = env.environment()
        self.config = environment.config()

        self.pub_endpoint = 'https://coincheck.com/'
        self.pri_endpoint = 'https://coincheck.com/'
        self.pair = environment.pair

        self.requet_header = {
            'content-type': 'application/json'
        }


    # Public API
    # last 最後の取引の価格
    # bid 現在の買い注文の最高価格
    # ask 現在の売り注文の最安価格
    # high 24時間での最高取引価格
    # low 24時間での最安取引価格
    # volume 24時間での取引量
    # timestamp 現在の時刻
    def getTicker(self):
        endpoint = 'api/ticker'
        url = str(self.pub_endpoint + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    # Public API
    # asks 売り注文の情報
    # bids 買い注文の情報
    def getOrderbooks(self):
        endpoint = 'api/order_books'
        url = str(self.pri_endpoint + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    def postSell(self):
        endpoint = 'api/exchange/orders'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'rate': 30000,
            'amount': 10,
            'order_type': "sell",
            'pair': self.pair
        }

        self.setRequestHeader(url, params)

        result = requests.post(url, params = params, headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def postBuy(self):
        endpoint = 'api/exchange/orders'
        url = str(self.pri_endpoint + endpoint)

        params = {
            'rate': 30000,
            'amount': 10,
            'order_type': "buy",
            'pair': self.pair
        }

        self.setRequestHeader(url, params)

        result = requests.post(url, params = params, headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def postOrderOpens(self):
        endpoint = 'api/exchange/orders/opens'
        url = str(self.pri_endpoint + endpoint)
        self.setRequestHeader(url)

        result = requests.get(url, headers = self.requet_header)
        obj = json.loads(result.content)

        return obj

    def setRequestHeader(self, path: str, params = None):
        nonce = str(round(time.time() * 1000000))
        message = nonce + path
        if params:
            message += '?' + urllib.parse.urlencode(params)

        signature = hmac.new(self.config['private']['CoinCheck']['api_secret'].encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        self.requet_header.setdefault('ACCESS-NONCE', nonce)
        self.requet_header.setdefault('ACCESS-KEY', self.config['private']['CoinCheck']['access_key'])
        self.requet_header.setdefault('ACCESS-SIGNATURE', signature)

        print('> SET REQUEST HEADERS : CoinCheck > ' + json.dumps(self.requet_header))
        logging.info('> SET REQUEST HEADERS : CoinCheck > ' + json.dumps(self.requet_header))
