from config import *
import requests
from urllib.parse import urljoin
import time

baseUrl = "https://fapi.binance.com/"

def getCandles (symbol,interval,limit):
    params = {
        "symbol" : symbol,
        "interval" : interval,
        "limit" : limit,
    }
    url = urljoin(baseUrl,"fapi/v1/klines")
    response = requests.get(url, params).json()
    print(response)
    return response


def getCloseTimes (symbol,intervalmin):
    candleCount = int((60 / intervalmin) * 24 * 3)
    interval = str(intervalmin) + "m"
    candles = getCandles(symbol,interval,candleCount)
    closeTimes = []
    for candles in candles :
        closeTime = float(candles[4])
        closeTimes.append(closeTime)
    return closeTimes

def calculateEma(data,day):
    emaValues = []
    multiplier = 2 / (day + 1)
    initialEma = sum(data[:day]) / day
    emaValues.append(initialEma)
    for i in range(day, len(data)):
        ema = (data[i] - emaValues[-1]) * multiplier + emaValues[-1]
        emaValues.append(ema)
    return emaValues


def calculatEmaValues () :
    dayOfEma = [5,8,13]
    emaDatasOfDays = []
    for day in dayOfEma :
        dataofDay = getCloseTimes("btcusdt",15)
        emaDataOfDay = calculateEma(dataofDay,day)
        emaDatasOfDays.append(emaDataOfDay)
    return emaDatasOfDays
    

def isCrossEmaValues ():
    emaValues = calculatEmaValues ()
    ema5Last = emaValues[0][-2]
    ema8Last = emaValues[1][-2]
    ema13Last = emaValues[2][-2]
    ema5SecondLast = emaValues[0][-3]
    ema8SecondLast = emaValues[1][-3]
    ema13SecondLast = emaValues[2][-3]
    if ema5SecondLast > ema8SecondLast or ema5SecondLast > ema13SecondLast: 
        if ema5Last < ema8Last and ema13Last:
            print("SHORTLA ")
    elif ema5SecondLast < ema8SecondLast or ema5SecondLast < ema13SecondLast :
        if ema5Last > ema8Last and ema13Last:
            print("LONGLA")

isCrossEmaValues()


    

