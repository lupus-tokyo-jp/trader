# encode=UTF-8
import logging
import pprint
import json
import classes.api.BitBank
import classes.api.CoinCheck

class Base:

    def __init__(self):
        self.BitBank = classes.api.BitBank.BitBankAPI()
        self.CoinCheck = classes.api.CoinCheck.CoinCheckAPI()

    def trade(self, config):
        depths = self.getDepthAll()
        pprint.pprint(depths)
        print('trade runnning.')

    def getDepthAll(self):
        depths = {}
        depths['BitBank'] = self.BitBank.getDepth()
        depths['CoinCheck'] = self.CoinCheck.getOrderbook()

        return depths

