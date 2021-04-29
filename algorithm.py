from binance.client import Client
import math
import time

class Algorithm:
    def __init__(self, klines):
        self.klines = klines
        self.responseDict = {"openTime": 0, "close": 4}

        self.candlesDict = {}
        self.candlesDictPriceF = {}
        self.timeStamps = []
        self.prices = []

        for i in klines:
            priceVal = round(float(i[self.responseDict["close"]]), 7 - int(math.floor(math.log10(abs(float(i[self.responseDict["close"]]))))) - 1)

            self.candlesDict[i[self.responseDict["openTime"]]] = priceVal
            self.candlesDictPriceF[priceVal] = i[self.responseDict["openTime"]]
            self.prices.append(priceVal)
            self.timeStamps.append(i[self.responseDict["openTime"]])

    def AddCandle(self, candle):
        self.klines.append(candle)

        for i in self.klines:
            priceVal = round(float(i[self.responseDict["close"]]), 7 - int(math.floor(math.log10(abs(float(i[self.responseDict["close"]]))))) - 1)

            self.candlesDict[i[self.responseDict["openTime"]]] = priceVal
            self.candlesDictPriceF[priceVal] = i[self.responseDict["openTime"]]
            self.prices.append(priceVal)
            self.timeStamps.append(i[self.responseDict["openTime"]])

    def CalculateMovingAverage(self, k):
        start = 0
        sums = []
        # Sliding Window SMA formula
        for i in self.prices:
            start += 1
            num = i
            subArr = self.prices[start:]
            kVals = subArr[:k-1]
            for j in kVals:
                num += j     

            num = num/k
            # num = round(num, 7 - int(math.floor(math.log10(abs(num)))) - 1)
            sums.append(num)

        val = k-1
        sums = sums[:len(self.prices) - (k - 1)]
        prices = self.prices[k-1:]

        # k value override
        tempPrices = prices
        if k == 7:
            for i in range(13):
                tempPrices.pop(0)
                sums.pop(0)

        # Form dictonary for sma values with timestamps
        result = {}
        for price, averagedPrice, timestamp in zip(tempPrices, sums, self.timeStamps):       
            timeStamp = timestamp
            result[timeStamp] = averagedPrice
        
        return result

