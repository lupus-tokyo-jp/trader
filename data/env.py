# encode=UTF-8

class environment:
    def __init__(self):
        self.base_path = '/srv/trade/'
        self.log_path = self.base_path + 'log/'
        self.log_conf = self.base_path + 'logging.conf'

        # Batch実行させる
        self.batch = 'false'

    # 定義
    def config(self):
        confd = {}
        confd['private'] = {
            'test' : 'test message'
        }

        return confd
