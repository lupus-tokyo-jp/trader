# encode=UTF-8
import logging
import pprint
import json
import api.BitBank
import api.CoinCheck

class Base:

    def __init__(self):
        self.BitBank = api.BitBank.BitBankAPI()
        self.CoinCheck = api.CoinCheck.CoinCheckAPI()

    def trade(self, config):
        print('trade runnning.')