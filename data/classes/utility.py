# encode=UTF-8
import sys
import logging
import pprint
import json
import importlib

import env

class Utility():
    def __init__(self):
        environment = env.environment()
        self.config = environment.config()

    # Perform print output and log output
    def outputInfo(self, class_name: str, method_name: str, msg):
        if not isinstance(msg, (int, str)):
            msg = json.dumps(msg)

        messages = class_name + ' > ' + method_name + ' : ' + msg

        print(messages)
        logging.info(messages)
