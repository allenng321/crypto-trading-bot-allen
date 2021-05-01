from binance.client import Client
from algorithm import Algorithm
import time
from datetime import datetime
from client import Binance
import math

api_key = "Kyrrk8yLOuql7it4CV4U8xV1IWog5sqWVzvJLqkYFtw9Gv3mCyYMRZgP0GSuzc52"
api_secret = "EbVbF6JX7WtzYdqLRnNCwwtX0jMrRzge1zowo4shxrAEG9YajLn1VVXn6m1Q9uCP"

client = Client(api_key, api_secret)

# klines1 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619065859", limit=1000)
# klines2 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619125859", limit=1000)
# klines3 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619185859", limit=1000)
# klines4 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619245859", limit=1000)
# klines5 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619305859", limit=1000)
# klines6 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619365859", limit=1000)
# klines7 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619425859", limit=1000)
# klines8 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619485859", limit=1000)
# klines9 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619545859", limit=1000)
# klines10 = client.get_historical_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, start_str="1619605859", limit=1000)
rawKlines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=1000)

# klines = klines1 + klines2 + klines3 + klines4 + klines5 + klines6 + klines7 + klines8 + klines9 + klines10

# klines = {}
# for i in rawKlines:
#     date = datetime.fromtimestamp(int(str(i[0])[:10]))
#     print(str(date))
#     klines[i[0]] = i[4]

# print(klines)

# movingAverages = [[10, 25], [10, 50], [10, 75], [10, 100], [10, 125], [10, 150], [10, 175], [10, 200], [10, 225], [10, 250], [25, 50], [25, 75], [25, 100], [25, 125], [25, 150],
# [25, 175], [25, 200], [25, 225], [25, 250], [50, 75], [50, 100], [50, 125], [50, 150], [50, 175], [50, 200], [50, 225], [50, 250], [75, 100], [75, 125], [75, 150], [75, 175],
# [75, 200],  [75, 225], [75, 250], [100, 125], [100, 150], [100, 175], [100, 200], [100, 225], [100, 250], [125, 150], [125, 175], [125, 200], [150, 175], [150, 200], [150, 225],
# [150, 250], [175, 200], [175, 225], [175, 250]
# ]

movingAverages = [[125, 150], [50, 100]]

Algorithm = Algorithm(rawKlines)

orginalPrice = {}
for i in rawKlines:
    price = round(float(i[4]), 7 - int(math.floor(math.log10(abs(float(i[4]))))) - 1)
    orginalPrice[i[0]] = price

# 125 150
sevenListF = Algorithm.CalculateMovingAverage(50)
twentyListF = Algorithm.CalculateMovingAverage(100)
sevenListS = Algorithm.CalculateMovingAverage(125)
twentyListS = Algorithm.CalculateMovingAverage(150)

# sevenListF, twentyListF, sevenListS, twentyListS = [], [], [], []
# for i, j, k, l in zip(sevenListFDict.values(), twentyListFDict.values(), sevenListSDict.values(), twentyListSDict.values()):
#     sevenListF.append(i)
#     twentyListF.append(j)
#     sevenListS.append(k)
#     twentyListS.append(l)

for i in range(50):
    sevenListF.pop(0)
for i in range(25):
    sevenListS.pop(0)

binanceClientF = Binance(2000)
binanceClientS = Binance(2000)

sevenHigherF = False
twentyHigherF = False

for i, j in zip(sevenListF, twentyListF):
    if j > i:
        twentyHigherF = True
        sevenHigherF = False
    elif i > j:
        sevenHigherF = True
        twentyHigherF = False

sevenHigherS = False
twentyHigherS = False

for i, j in zip(sevenListS, twentyListS):
    if j > i:
        twentyHigherS = True
        sevenHigherS = False
    elif i > j:
        print(str(i) + " > " + str(j))
        sevenHigherS = True
        twentyHigherS = False

print("stops")

while True:
    time.sleep(60)

    latestCandles = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=1000)
    price = round(float(latestCandles[-1][4]), 7 - int(math.floor(math.log10(abs(float(latestCandles[-1][4]))))) - 1)
    orginalPrice[latestCandles[-1][0]] = price
    timestamp = latestCandles[-1][0]

    Algorithm.AddCandle(latestCandles)

    sevenListF = []
    twentyListF = []
    sevenListF = Algorithm.CalculateMovingAverage(50)
    twentyListF = Algorithm.CalculateMovingAverage(100)

    sevenListS = []
    twentyListS = []
    sevenListS = Algorithm.CalculateMovingAverage(125)
    twentyListS = Algorithm.CalculateMovingAverage(150)

    for i in range(50):
        sevenListF.pop(0)
    for i in range(25):
        sevenListS.pop(0)
    
    date = datetime.fromtimestamp(int(str(timestamp)[:10]))
    print("For 50 100: Time: " + str(date) + " Seven: " + str(sevenListF[-1]) + " Twenty: " + str(twentyListF[-1]))

    date = datetime.fromtimestamp(int(str(timestamp)[:10]))
    print("For 125 150: Time: " + str(date) + " Seven: " + str(sevenListS[-1]) + " Twenty: " + str(twentyListS[-1]))

    

    sevenHigherFAdded = False
    twentyHigherFAdded = False

    for i, j in zip(sevenListF, twentyListF):
        if j > i:
            twentyHigherFAdded = True
            sevenHigherFAdded = False
        elif i > j:
            sevenHigherFAdded = True
            twentyHigherFAdded = False

    if twentyHigherFAdded and sevenHigherF:
        sevenHigherF = False
        twentyHigherF = True
        binanceClientS.Sell(orginalPrice[timestamp], timestamp, 1, " 50, 100")
        # binanceClientF.Short(orginalPrice[timestamp], timestamp, 1, " 50, 100")
    elif twentyHigherF and sevenHigherFAdded:
        sevenHigherF = True
        twentyHigherF = False
        if binanceClientF.isBought:
            binanceClientF.Buy(orginalPrice[timestamp], timestamp, 1, " 50, 100")
        # if binanceClientF.isShorted:
        #     binanceClientF.CloseShort(orginalPrice[timestamp], timestamp, " 50, 100")

    print(sevenHigherF)
    print(twentyHigherF)
    print(sevenHigherFAdded)
    print(twentyHigherFAdded)

    sevenHigherSAdded = False
    twentyHigherSAdded = False

    for i, j in zip(sevenListS, twentyListS):
        if j > i:
            twentyHigherSAdded = True
            sevenHigherSAdded = False
        elif i > j:
            sevenHigherSAdded = True
            twentyHigherSAdded = False

    if twentyHigherSAdded and sevenHigherS:
        sevenHigherS = False
        twentyHigherS = True
        binanceClientS.Sell(orginalPrice[timestamp], timestamp, 1, " 125, 150")
        # binanceClientS.Short(orginalPrice[timestamp], timestamp, 1, " 125, 150")
    elif twentyHigherS and sevenHigherFAdded:
        sevenHigherS = True
        twentyHigherS = False
        if binanceClientS.isBought:
            binanceClientS.Buy(orginalPrice[timestamp], timestamp, 1, " 125, 150")
        # if binanceClientS.isShorted:
        #     binanceClientS.CloseShort(orginalPrice[timestamp], timestamp, " 125, 150")
    print("-------")
    print(sevenHigherS)
    print(twentyHigherS)
    print(sevenHigherSAdded)
    print(twentyHigherSAdded)
    
    print("Waiting for next action...")

# finalBalances = []

# for pair in movingAverages:
#     print("Moving Average for result below: " + str(pair[0]) + " " + str(pair[1]))
    
#     binanceClient = Binance(2000)
    
#     orginalPrice = {}
#     for i in klines:
#         price = round(float(i[4]), 7 - int(math.floor(math.log10(abs(float(i[4]))))) - 1)
#         orginalPrice[i[0]] = price

#     sevenList = Algorithm.CalculateMovingAverage(pair[0])
#     twentyList = Algorithm.CalculateMovingAverage(pair[1])

#     sevenHigher = False
#     twentyHigher = False



#     for i, j in zip(sevenList, twentyList):
#         if twentyList[j] > sevenList[i]:
#             twentyHigher = True
#             continue
#         elif sevenList[i] > twentyList[j]:
#             #sevenHigher = True
#             continue
#         break

#     for i, j, k in zip(sevenList, twentyList, orginalPrice):
#         if sevenHigher and not twentyHigher:
#             if twentyList[j] > sevenList[i]: 
#                 # print("Buy Signal at " + str(i))
#                 # binanceClient.Buy(orginalPrice[j], 1)
#                 # binanceClient.Short(orginalPrice[k], i, 1)
#                 binanceClient.CloseShort(orginalPrice[k], i)
#                 twentyHigher = True
#                 sevenHigher = False
#         elif twentyHigher and not sevenHigher:
#             if sevenList[i] > twentyList[j]:
#                 # print("Sell Signal at " + str(j))
#                 # binanceClient.Sell(orginalPrice[j], i)
#                 # binanceClient.CloseShort(orginalPrice[k], i)
#                 binanceClient.Short(orginalPrice[k], i, 1)
#                 twentyHigher = False
#                 sevenHigher = True

#     if binanceClient.balance == 0:
#         finalBalances.append(binanceClient.soldOriginalBalance)
#     else:
#         finalBalances.append(binanceClient.balance)
#     print("Moving Average for result above: " + str(pair[0]) + " " + str(pair[1]))

# print("Final result below")
# for i, j in zip(finalBalances, movingAverages):
#     print(str(i))
#     percentage = ((i / 2000) - 1) * 100

#     percentage = round(float(percentage), 3 - int(math.floor(math.log10(abs(percentage)))) - 1)

#     print("For {}, Final Balance: {}, Percentage: {}".format(str(j), str(i), str(percentage)))