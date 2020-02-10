# encode=UTF-8
import logging
import pprint
import json
import coincheck.market
import python_bitbankcc

class base:

    def __init__(self):
        # 取引範囲
        self.allow = int(1000)

        # BitBank
        self.bb_pub = python_bitbankcc.public()

        # CoinCheck
        self.cm1 = coincheck.market.Market()

    def ticker(self):
        buy = {}
        sell = {}

        # BitBank
        bb_t = self.bb_pub.get_ticker(
            'btc_jpy'
        )
        buy.setdefault("BitBank", int(bb_t["buy"]))
        sell.setdefault("BitBank", int(bb_t["sell"]))

        print("BitBank >")
        pprint.pprint(bb_t)

        # CoinCheck
        cc_t = self.cm1.ticker()
        buy.setdefault("Coinckeck", int(cc_t["bid"]))
        sell.setdefault("Coinckeck", int(cc_t["ask"]))

        print("CoinCheck >")
        pprint.pprint(cc_t)

        print("BUY >")
        pprint.pprint(buy)
        print("SELL >")
        pprint.pprint(sell)

        # dictinary check
        pprint.pprint("BUY MAX: " + max(buy, key=buy.get))
        pprint.pprint("BUY MIN: " + min(buy, key=buy.get))
        pprint.pprint("SELL MAX: " + max(sell, key=sell.get))
        pprint.pprint("SELL MIN: " + min(sell, key=sell.get))

        # trade
        if min(sell, key=sell.get) != max(buy, key=buy.get):
            print(min(sell, key=sell.get) + "(" + str(min(sell.values())) + ")" + "から購入して" + max(buy, key=buy.get)+ "(" + str(max(buy.values())) + ")" + "で売る")
            print("差分:" + str(max(buy.values()) - min(sell.values())))

            if int(max(buy.values()) - min(sell.values())) < self.allow:
                print("最低取引額（" + str(self.allow) + "）より差分が低いので取引しまてーん")

        else:
            print("取引しない")
