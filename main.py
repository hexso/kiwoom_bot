from kiwoom_api import *
from PyQt5.QtWidgets import QApplication
from telegram_bot import TelegramBot
from time import sleep
import sys
import logging


class AutoBot:

    def __init__(self):
        self.kiwoom = KiwoomApi()
        # 로그 생성
        self.logger = logging.getLogger()

        # 로그의 출력 기준 설정
        self.logger.setLevel(logging.INFO)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # log 출력
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # log를 파일에 출력
        file_handler = logging.FileHandler('my.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        res = self.kiwoom.login()
        if res is False:
            self.logger.info('로그인 실패')
            return False
        self.logger.info('로그인 성공')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot = AutoBot()
    tgBot = TelegramBot()
    if bot is False or tgBot is False:
        sys.exit()


    app.exec()