# encode=UTF-8

class environment:
    def __init__(self):
        self.base_path = '/srv/trade/'
        self.log_path = self.base_path + 'strage/log/'
        self.log_conf = self.log_path + 'logging.conf'

        # Batch実行させる
        self.batch = 'false'

        # 取引所の設定
        self.exchange = [
            'BitBank',
            'CoinCheck'
        ]

    # 定義
    def config(self):
        confd = {}

        # 取引範囲
        confd['allow'] = 1000

        # 個人設定
        confd['private'] = {
            'test' : 'test message'
        }

        return confd
