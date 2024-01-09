from config import *
import requests
from urllib.parse import urljoin

baseUrl = "https://fapi.binance.com/"

def getCandles (symbol,interval,limit):
    params = {
        "symbol" : symbol,
        "interval" : interval,
        "limit" : limit
    }

    url = urljoin(baseUrl,"fapi/v1/klines")
    response = requests.get(url, params).json()
    return response

def calculateCloseTimes (symbol,day,intervalmin):
    candleCount = int((60 / intervalmin) * 24 * day)
    interval = str(intervalmin) + "m"
    testo = getCandles(symbol,interval,candleCount)
    closeTimes = []
    for candles in testo :
        closeTime = float(candles[4])
        closeTimes.append(closeTime)
    return closeTimes

def calculate_ema(data,period):
    ema_values = []
    multiplier = 2 / (period + 1)
    
    # İlk EMA değeri, veri setinin ortalaması ile başlar
    initial_ema = sum(data[:period]) / period
    ema_values.append(initial_ema)
    
    # Diğer EMA değerleri hesaplanır
    for i in range(period, len(data)):
        ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)
    print(ema_values)
    return ema_values

data = calculateCloseTimes("btcusdt",5,15)    
period = 5  
calculate_ema(data,period)


