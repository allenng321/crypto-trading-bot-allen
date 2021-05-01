from datetime import datetime

class Binance:
    def __init__(self, balance):
        self.balance = balance
        self.btc = 0
        self.pay = 0
        self.shortedPrice = 0
        self.soldOriginalBalance = 0
        self.isShorted = False
        self.isBought = False

    def Buy(self, price, timeStamp, suffix):
        buyingBalance = self.balance * margin
        self.btc = buyingBalance / price
        self.pay = (self.balance * margin) - self.balance
        self.balance = 0

        self.isBought = True

        date = datetime.fromtimestamp(int(str(timeStamp)[:10]))
        print("Bought at " + str(price) + " Timestamp: " + str(timeStamp) + " " + suffix)

    def Sell(self, price, timeStamp, sufix):
        soldBalance = (self.btc * price) - self.pay
        self.btc, self.pay = 0, 0
        self.balance = soldBalance
        date = datetime.fromtimestamp(int(str(timeStamp)[:10]))
        print("Sold at " + str(price) + " balance: " + str(self.balance) + " Timestamp: " + str(date) + suffix)

    def Short(self, price, timeStamp, margin, suffix):
        self.isShorted = True
        self.btc = (self.balance * margin) / price
        self.pay = (self.balance * margin) - self.balance
        self.shortedPrice, self.soldOriginalBalance = price, self.balance
        self.balance = 0

        date = datetime.fromtimestamp(int(str(timeStamp)[:10]))
        print("Shorted at " + str(price) + " Timestamp: " + str(date) + suffix)

    def CloseShort(self, price, timeStamp, suffix):
        buyBackBalance = (self.btc * price) - self.pay
        self.balance = self.soldOriginalBalance + (self.soldOriginalBalance - buyBackBalance)
        self.btc, self.pay = 0, 0

        date = datetime.fromtimestamp(int(str(timeStamp)[:10]))
        print("Closed Short at " + str(price) + " balance: " + str(self.balance) + " Timestamp: " + str(date) + suffix)
    