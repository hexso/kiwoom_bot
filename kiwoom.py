import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Kiwoom(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        #event 셋팅
        self.kiwoom.OnEventConnect.connect(self.login_event)
        self.kiwoom.OnReceiveTrData.connect(self.tr_slot)


        self.getRapidTradeRateEventLoop = QEventLoop()
        self.latestData = None
        self.login_event_loop = None

    def login(self):
        self.kiwoom.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def login_event(self, err_code):
        if err_code == 0:
            print("로그인 성공")
        else:
            print(err_code)
        self.login_event_loop.exit()

    def tr_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):
        if sRQName == '거래량급증요청':
            self.onGetRapidTradeRate(sTrCode, sRQName, sRecordName)

    def onGetRapidTradeRate(self, sTrCode, sRQName, sRecordName):
        rows = self.getRepeatCnt(sTrCode, sRQName)
        cnt = 0
        self.latestData = []
        if rows == 0:
            print('rapid trade rate 데이터를 받지 못했습니다.')
        for idx in range(rows):
            code = self.kiwoom.GetCommData(sTrCode, sRQName, idx, "종목코드").strip()
            code_name = self.kiwoom.GetCommData(sTrCode, sRQName, idx, "종목명").strip()
            now_price = int(self.kiwoom.GetCommData(sTrCode, sRQName, idx, "현재가").strip())
            order_quantity = int(self.kiwoom.GetCommData(sTrCode, sRQName, idx, "전일대비").strip())
            before_trade_amount = int(self.kiwoom.GetCommData(sTrCode, sRQName, idx, "이전거래량").strip())
            now_trade_amount = int(self.kiwoom.GetCommData(sTrCode, sRQName, idx, "현재거래량").strip())
            rapid_amount = int(self.kiwoom.GetCommData(sTrCode, sRQName, idx, "급증량").strip())
            rapid_rate = self.kiwoom.GetCommData(sTrCode, sRQName, idx, "급증률").strip()
            price_rate_percent = self.kiwoom.GetCommData(sTrCode, sRQName, idx, "등락률").strip()
            dic = {'종목코드':code, '종목명':code_name, '현재가':now_price,'전일대비':order_quantity,
                                    '이전거래량':before_trade_amount, '현재거래량':now_trade_amount,
                                    '급증량':rapid_amount, '급증률':rapid_rate, '등락률':price_rate_percent}
            self.latestData.append(dic)
        self.getRapidTradeRateEventLoop.exit()

    def getRapidTradeRate(self):
        self.setInputValue('시장구분','000')
        self.setInputValue('정렬구분','2')
        self.setInputValue('시간구분','2')
        self.setInputValue('거래량구분','500')
        self.setInputValue('시간','1')
        self.setInputValue('종목조건','0')
        self.setInputValue('가격구분','0')
        self.commRqData('거래량급증요청', 'OPT10023','0','0000')
        self.getRapidTradeRateEventLoop.exec_()

    def setInputValue(self, name, value):
        '''
        :param name: TR에 명시된 Input이름
        :param value: Input이름으로 지정한 값
        :return:
        '''
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", name, value)

    def commRqData(self, sRQName, sTrCode, sPrevNext, sScrNo):
        '''
        :param sRQName: 사용자 구분명
        :param sTrCode: 조회하려는 TR이름
        :param sPrevNext: 연속조회여부
        :param sScrNo: 화면번호
        :return:
        '''
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString", sRQName, sTrCode, sPrevNext, sScrNo)

    def getRepeatCnt(self, sTrCode, sRQName):
        '''
        :param sTrCode: TR 이름
        :param sRQName: 레코드 이름 한번에 최대 900개 데이터를 수신
        :return:
        '''
        return self.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)

    def getData(self):
        return self.latestData

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.login()
    kiwoom.getRapidTradeRate()
    data=kiwoom.getData()
    print(data)
    app.exec()