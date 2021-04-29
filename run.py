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
rawKlines = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=200)

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

sevenListF = Algorithm.CalculateMovingAverage(125)
twentyListF = Algorithm.CalculateMovingAverage(150)
sevenListS = Algorithm.CalculateMovingAverage(50)
twentyListS = Algorithm.CalculateMovingAverage(100)

binanceClientF = Binance(2000)
binanceClientS = Binance(2000)

sevenHigherF = False
twentyHigherF = False

for i, j in zip(sevenListF, twentyListF):
    if twentyListF[j] > sevenListF[i]:
        twentyHigherF = True
        sevenHigherF = False
    elif sevenListF[i] > twentyListF[j]:
        sevenHigherF = True
        twentyHigherF = False

while True:
    time.sleep(60)

    latestCandle = client.get_klines(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)
    price = round(float(latestCandle[0][4]), 7 - int(math.floor(math.log10(abs(float(latestCandle[0][4]))))) - 1)
    orginalPrice[latestCandle[0][0]] = price
    timestamp = latestCandle[0][0]

    Algorithm.AddCandle(latestCandle[0])
    sevenListF = Algorithm.CalculateMovingAverage(125)
    twentyListF = Algorithm.CalculateMovingAverage(150)

    sevenHigherFAdded = False
    twentyHigherFAdded = False

    for i, j, k in zip(sevenListF, twentyListF, orginalPrice):
        if twentyListF[j] > sevenListF[i]:
            twentyHigherFAdded = True
            sevenHigherFAdded = False
        elif sevenListF[i] > twentyListF[j]:
            sevenHigherFAdded = True
            twentyHigherFAdded = False
    
    print(twentyHigherFAdded)
    print(sevenHigherFAdded)
    print(twentyHigherF)
    print(sevenHigherF)

    if twentyHigherFAdded and sevenHigherF:
        sevenHigherF = False
        twentyHigherF = True
        binanceClientF.Short(orginalPrice[timestamp], timestamp, 1, "F")
    elif twentyHigherF and sevenHigherFAdded:
        sevenHigherF = True
        twentyHigherF = False
        binanceClientF.CloseShort(orginalPrice[timestamp], timestamp, "F")
    
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