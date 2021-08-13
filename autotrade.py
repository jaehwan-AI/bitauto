import os
import time
import pyupbit
import datetime

from inference import inference


access = "6zx2diWSu3Ad7I5z9maXjCYT7x5xZWGtnI4U3mtO"          # personal value
secret = "e5Hp9qfxVCULo65ysIHxXFDy5ui9IEOxUCLSxK0j"          # personal value

def get_start_time(ticker):
    ''' start time '''
    df = pyupbit.get_ohlcv(ticker, interval='day', count=1)
    start_time = df.index[0]
    return start_time

# def get_balance(ticker):
#     ''' get balance '''
#     balances = upbit.get_balance()
#     print(balances)
#     for b in balances:
#         if b['currency'] == ticker:
#             if b['balance'] is not None:
#                 return float(b['balance'])
#             else:
#                 return 0

def get_current_price(ticker):
    ''' current price '''
    return pyupbit.get_orderbook(tickers=ticker)[0]['orderbook_units'][0]['ask_price']


# login
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# BTC / ETH / LINK
ticker = "KRW-BTC"
tic = "BTC"

# now = datetime.datetime.now()
# start_time = get_start_time(ticker)
# end_time = start_time + datetime.timedelta(hours=12)

# current_price = get_current_price(ticker)

# btc = upbit.get_balance(tic)
# krw = upbit.get_balance("KRW")

# print(end_time)
# print('-'*20)
# print(current_price)
# print('-'*20)
# print(btc, krw)

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
