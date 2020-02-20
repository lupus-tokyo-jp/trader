# encode=UTF-8
import logging
import pprint
import pprint
import json
import requests
import time
import hashlib
import hmac

import env

class CoinCheckAPI:
    def __init__(self):
        # Load env.
        environment = env.environment()
        self.config = environment.config()

        self.pub_endpoint = 'https://coincheck.com/'
        self.pair = 'btc_jpy'

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
        endpoint = '/api/order_books'
        url = str(self.pub_endpoint + endpoint)

        response = requests.get(url)
        obj = json.loads(response.content)
        return obj

    def postSell(self):
        endpoint = '/api/exchange/orders'
        url = str(self.pub_endpoint + endpoint)

        header = self.getRequestHeader(endpoint);
        print(header)

        msg = "Coincheck sell"
        return msg

    def postBuy(self):
        msg = "Coincheck buy"
        return msg

    def getRequestHeader(self, path: str):
        nonce = str(round(time.time() * 1000000))
        url = 'https://' + self.pub_endpoint + path
        message = nonce + url

        signature = hmac.new(self.config['private']['CoinCheck']['access_key'].encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        header = {
                'ACCESS-NONCE': nonce,
                'ACCESS-KEY': self.config['private']['CoinCheck']['access_key'],
                'ACCESS-SIGNATURE': signature
            }

        return header

    def privateRequest(self, header):
