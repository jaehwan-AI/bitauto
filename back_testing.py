import datetime
import os
import time

import pyupbit

from inference import predict_arima, predict_prophet


def get_start_time(ticker):
    ''' start time '''
    df = pyupbit.get_ohlcv(ticker, interval='day', count=1)
    start_time = df.index[0]
    return start_time


def get_current_price(ticker):
    ''' current price '''
    return pyupbit.get_orderbook(ticker=ticker)['orderbook_units'][0]['ask_price']


# BTC / ETH / LINK
ticker = "KRW-BTC"
tic = "BTC"

now = datetime.datetime.now()
start_time = get_start_time(ticker)
end_time = start_time + datetime.timedelta(hours=12)

current_price = get_current_price(ticker)
print(current_price)


'''
# start auto trade
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(hours=12)

        # 09:00 ~ 21:00
        if start_time < now < end_time:
            # training model


            # predict_price
            predict_price = inference(ticker)
            current_price = get_current_price(ticker)

            if predict_price < current_price:
                btc = upbit.get_balance(tic)
                if btc > 0.00008:
                    upbit.sell_market_order(ticker, btc*0.9995) # 수수료 0.05 고려
            else:
                krw = upbit.get_balance("KRW")
                if krw > 5000: # 최소 주문 가능 금액
                    upbit.buy_market_order(ticker, krw*0.9995) # 수수료 0.05 고려
        else:
            # os.system("shutdown -s -f")
            break
    except Exception as e:
        print(e)
        break
'''
