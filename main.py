from kiwoom import *
from PyQt5.QtWidgets import QApplication
from telegram_bot import TelegramBot
import schedule
from time import sleep
import sys

class AutoBot():
    def __init__(self):
        self.tgBot = TelegramBot()
        self.kiwoom = Kiwoom()

    def telegramLogin(self):
        with open('private.txt', 'r') as f:
            data = f.read()
            data = data.split('\n')
            for i in data:
                if 'telegramtoken' in i:
                    token = i[i.find(':') + 1:]
                elif 'telegramchatid' in i:
                    chatid = i[i.find(':') + 1:]
        self.tgBot.SetChatId(chatid)
        self.tgBot.SetToken(token)
        self.tgBot.SendMsg('텔레그램 로그인 완료')

    def kiwoomLogin(self):
        self.kiwoom.login()

    def sendRapidInfo(self):
        self.kiwoom.getRapidTradeRate()
        datas = self.kiwoom.getData()
        wanted_datas = []
        for data in datas:
            rapid_rate = float(data['등락률'])
            if 10 > rapid_rate > 0:
                wanted_datas.append(data)

        msgs = ''
        for data in wanted_datas:
            msg = '종목명 : {}  ,이전거래량 : {}   , 현재거래량 : {}   , 급증률 : {},  등락률 : {}  \n'.format(
                data['종목명'],data['이전거래량'],data['현재거래량'], data['급증률'], data['등락률'])
            msgs +=msg
            if len(msgs) > 3000:
                self.tgBot.SendMsg(msgs)
                msgs = ''
                sleep(1)
        self.tgBot.SendMsg(msgs)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot = AutoBot()
    bot.telegramLogin()
    bot.kiwoomLogin()
    # schedule.every().day.at("15:30").do(bot.sendRapidInfo)
    # while True:
    #     schedule.run_pending()
    #     sleep(1)
    #bot.sendRapidInfo()

    app.exec()