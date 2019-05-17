#!/usr/bin/env python3
import sys
import requests
import datetime
from googlevoice import Voice

log = open("/Users/nshah/PycharmProjects/StockAlerts/stockAlerts.log", "a")
sys.stdout = log
print ("Start " + str(datetime.datetime.now()))

voice = Voice()
voice.login("shah.nayan.m@gmail.com", "StockAlerts123")

round_5mins = 5
round_10mins = 10
now = datetime.datetime.now()
mins5 = now.minute - (now.minute % round_5mins)
dateTimeNearest5Min = str(datetime.datetime(now.year, now.month, now.day, now.hour + 3, mins5))[:-3]
dateTimeNearest10Min = str(datetime.datetime(now.year, now.month, now.day, now.hour + 3, mins5) - datetime.timedelta(minutes=5))[:-3]
print("dateTimeNearest5Min " + dateTimeNearest5Min)
print("dateTimeNearest10Min " + dateTimeNearest10Min)

apikey = "FQNM"
# apiKeys = ["FQNM", "1BRMFVOI45RA8EFC", "G1YTRRFMBBYDQX6T", "BXLDWMT70TUJFHS4", "LMV6TGJDJQNFQIOX", "CVQ3ZXDM2VSGHLNX"]
tickers = ["SPY", "TSLA"]
# "UGAZ", "UWTI", "GLD", "BA", "IWM", "QQQ", "VXX", "EWZ", "XLF", "XLV", "XLU", "AAPL", "AMZN", "GOOG", "MSFT", "FB", "NFLX", "NVDA", "TSLA"
for ticker in tickers:
    print("Working on " + ticker)

    ema9Resp = requests.get("https://www.alphavantage.co/query?function=EMA&interval=5min&time_period=9&series_type=open&symbol="+ticker+"&apikey="+apikey)
    if ema9Resp.status_code != 200:
        voice.send_sms(5102697649, "Stock Alerts API not returning ema9Response for "+ticker)
    ema9Data = ema9Resp.json()
    ema9Now = ema9Data["Technical Analysis: EMA"][dateTimeNearest5Min]["EMA"]
    print("ema9Now " + ema9Now)
    ema9Before = ema9Data["Technical Analysis: EMA"][dateTimeNearest10Min]["EMA"]
    print("ema9Before " + ema9Before)

    ema4Resp = requests.get("https://www.alphavantage.co/query?function=EMA&interval=5min&time_period=4&series_type=open&symbol="+ticker+"&apikey="+apikey)
    if ema4Resp.status_code != 200:
        voice.send_sms(5102697649, "Stock Alerts API not returning ema4Response for " + ticker)
    ema4Data = ema4Resp.json()
    ema4Now = ema4Data["Technical Analysis: EMA"][dateTimeNearest5Min]["EMA"]
    print("ema4Now " + ema4Now)
    ema4Before = ema4Data["Technical Analysis: EMA"][dateTimeNearest10Min]["EMA"]
    print("ema4Before " + ema4Before)

    if ema4Before >= ema9Before and ema4Now < ema9Now:
        voice.send_sms(5102697649, "SELL " + ticker)
        print("Sending SELL SMS for " + ticker)
    if ema4Before <= ema9Before and ema4Now > ema9Now:
        voice.send_sms(5102697649, "BUY " + ticker)
        print("Sending BUY SMS for " + ticker)

print ("End " + str(datetime.datetime.now()))
