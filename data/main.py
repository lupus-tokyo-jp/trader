# encode=UTF-8
import os
import sys
import datetime
import logging
import pprint
import classes.base
import env

def main():
    environment = env.environment()
    config = environment.config()
    print(config)

    args = sys.argv
    print(args)

    if len(args) == 2 and args[1] == 'batch' and environment.batch == 'true':
        base = classes.base.base()
        base.ticker()

    elif len(args) == 1:
        logging.info('Manual execution')

    else:
        sys.exit()
        # logging.info('run is cancel')

def makeLog(const):
    today = datetime.date.today()
    file_path = str(const.log_path) + str(today)

    # Logディレクトリがなければ作成する
    if not os.path.isdir(const.log_path):
        os.makedirs(const.log_path)

    return file_path

def initialize():
    const = env.environment()
    const.log_file = makeLog(const)

    return const

if __name__ == '__main__':
    const = initialize()

    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S',
        filename=const.log_file,
        level=logging.DEBUG
    )

    main()

