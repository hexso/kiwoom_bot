from kiwoom import Kiwoom
from time import time


SLEEP_TIME = 0.2


class KiwoomApi:

    def __init__(self):
        self.kiwoom = Kiwoom()

        if self.kiwoom.kiwoom_GetConnectState() is not 0:
            print('연결되지 않았음')
            return False
        self.account = self.get_account()

    def login(self):
        res = self.kiwoom.kiwoom_CommConnect()
        if res.get('result') is 0:
            print('로그인 성공')
            return True

        print('로그인 실패')
        return False

    def get_account(self):
        '''
        여러개의 계좌를 받을 수 있으나 기본적으로 1개로 한다.
        :return: 계좌번호
        '''
        accounts = self.kiwoom.kiwoom_GetAccList()
        return accounts[0]

    def get_balance(self):
        '''
        계좌의 남은 금액을 출력해준다.
        :return: 남은 금액
        '''
        self.kiwoom.kiwoom_TR_OPW00001_예수금상세현황요청(self.account)
        while not self.kiwoom.int_주문가능금액:
            time.sleep(SLEEP_TIME)
        balance = self.kiwoom.int_주문가능금액
        return balance
