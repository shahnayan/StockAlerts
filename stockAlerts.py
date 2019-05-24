#!/usr/bin/env python3
import sys
import requests
import datetime
from googlevoice import Voice

log = open("/Users/nshah/PycharmProjects/StockAlerts/stockAlerts.log", "a")
sys.stdout = log
print ("Start " + str(datetime.datetime.now()))

voice = Voice()
voice.login("shah.nayan.m@gmail.com", "StockAlert1234")

round_5mins = 5
round_10mins = 10
now = datetime.datetime.now()
mins5 = now.minute - (now.minute % round_5mins)
dateTimeNearest5Min = str(datetime.datetime(now.year, now.month, now.day, now.hour + 3, mins5))[:-3]
dateTimeNearest10Min = str(datetime.datetime(now.year, now.month, now.day, now.hour + 3, mins5) - datetime.timedelta(minutes=5))[:-3]
print("dateTimeNearest5Min " + dateTimeNearest5Min)
print("dateTimeNearest10Min " + dateTimeNearest10Min)

apikey = "AORKX5WZHKYNAT1F"
# apiKeys = ["FQNM", "1BRMFVOI45RA8EFC", "G1YTRRFMBBYDQX6T", "BXLDWMT70TUJFHS4", "LMV6TGJDJQNFQIOX", "CVQ3ZXDM2VSGHLNX"]
tickers = ["SPY", "PFE", "AAPL", "TSLA", "XLF", "XLV", "XLU", "JD", "XLP", "NFLX", "FXI", "AMZN", "BABA", "QCOM"]
supportResistance = dict({"SPY":"283.26, 284.74, 287.40, 291.24",  "PFE":"41.68, 42.23",  "AAPL":"185.47, 189.03, 191.32, 193.76",  "TSLA":"228.97",  "XLF":"26.33, 26.75, 26.96, 27.17",  "XLV":"87.14, 89.66",  "XLU":"58.25, 58.72",  "JD":"27.66, 28.25, 29.10",  "XLP":"57.25, 57.33",  "NFLX":"348.67, 358.42, 381.40",  "FXI":"40.48, 40.71",  "AMZN":"1778.03, 1993.53",  "BABA":"154.73, 161.95, 163.75",  "QCOM":"72.5, 77.88, 80.38"})
# "SPY", "TSLA", "UGAZ", "UWTI", "GLD", "BA", "IWM", "QQQ", "VXX", "EWZ", "XLF", "XLV", "XLU", "AAPL", "AMZN", "GOOG", "MSFT", "FB", "NFLX", "NVDA", "TSLA"
for ticker in tickers:
    print("Working on " + ticker)

    ema9Resp = requests.get("https://www.alphavantage.co/query?function=EMA&interval=5min&time_period=9&series_type=open&symbol="+ticker+"&apikey="+apikey)
    if ema9Resp.status_code != 200:
        voice.send_sms(5102697649, "Stock Alerts API not returning ema9Response for "+ticker)
    ema9Data = ema9Resp.json()
    try:
        ema9Now = ema9Data["Technical Analysis: EMA"][dateTimeNearest5Min]["EMA"]
        print("ema9Now " + ema9Now)
        ema9Before = ema9Data["Technical Analysis: EMA"][dateTimeNearest10Min]["EMA"]
        print("ema9Before " + ema9Before)
    except Exception as ex:
        voice.send_sms(5102697649, "ema9 not available for " + ticker)
        print("ema9 not available for " + ticker)

    ema4Resp = requests.get("https://www.alphavantage.co/query?function=EMA&interval=5min&time_period=4&series_type=open&symbol="+ticker+"&apikey="+apikey)
    if ema4Resp.status_code != 200:
        voice.send_sms(5102697649, "Stock Alerts API not returning ema4Response for " + ticker)
    ema4Data = ema4Resp.json()
    try:
        ema4Now = ema4Data["Technical Analysis: EMA"][dateTimeNearest5Min]["EMA"]
        print("ema4Now " + ema4Now)
        ema4Before = ema4Data["Technical Analysis: EMA"][dateTimeNearest10Min]["EMA"]
        print("ema4Before " + ema4Before)
    except Exception as ex:
        voice.send_sms(5102697649, "ema4 not available for " + ticker)
        print("ema4 not available for " + ticker)

    try:
        if ema4Before >= ema9Before and ema4Now < ema9Now:
            voice.send_sms(5102697649, "SELL " + ticker + ". Levels : " + supportResistance[ticker])
            print("Sending SELL SMS for " + ticker + ". Levels : " + supportResistance[ticker])
        if ema4Before <= ema9Before and ema4Now > ema9Now:
            voice.send_sms(5102697649, "BUY " + ticker + ". Levels : " + supportResistance[ticker])
            print("Sending BUY SMS for " + ticker + ". Levels : " + supportResistance[ticker])
    except NameError:
        print("One of the EMAs not available for " + ticker)

print ("End " + str(datetime.datetime.now()))
