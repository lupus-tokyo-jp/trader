# encode=UTF-8

class environment:
    def __init__(self):
        self.base_path = '/srv/trade/'
        self.log_path = self.base_path + 'strage/log/'
        self.log_conf = self.log_path + 'logging.conf'

        # Batch実行させる
        self.batch = 'false'

        # 取引所の設定
        self.exchanges = [
            'BitBank',
            'CoinCheck'
        ]

        self.pair = 'btc_jpy'

    # 定義
    def config(self):
        confd = {}

        # 取引範囲
        confd['allow'] = 1000

        # 個人設定
        confd['private'] = {
            'CoinCheck' : {
                'access_key' : 'ccxi8LmdUkscBLa6',
                'api_secret' : 'Nb5VkFMjjmwAvJ7tFeBBYDJhh9siM5nB'
            },
            'BitBank' : {
                'access_key' : 'a5c9dc2d-e023-4814-af9c-89c9928eab42',
                'api_secret' : '2a807fd82ce21cb3f182ce3207baa2e40e8182bc580bb9dea041cd3da8b749f9'
            }
        }

        return confd
