import datetime
import time

import pyupbit
import requests
import schedule

from inference import predict_arima, predict_prophet

# login
access = "6zx2diWSu3Ad7I5z9maXjCYT7x5xZWGtnI4U3mtO"          # personal value
secret = "e5Hp9qfxVCULo65ysIHxXFDy5ui9IEOxUCLSxK0j"          # personal value

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# BTC / ETH / LINK
ticker = "KRW-BTC"
tic = "BTC"

# slack
myToken = ""
def post_message(token, channel, text):
    '''post message to slack channel'''
    response = requests.post("https://slack.com/api/chat.postMessage",
        header = {"Authorization": "Bearer " + token},
        data = {"channel": channel, "text": text}
    )


def get_start_time(ticker):
    '''start time '''
    df = pyupbit.get_ohlcv(ticker, interval='day', count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    '''get balance '''
    balances = upbit.get_balance()
    print(balances)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    '''current price '''
    return pyupbit.get_orderbook(tickers=ticker)[0]['orderbook_units'][0]['ask_price']


future_price = 0
def predict_price(ticker):
    '''prediction future price'''
    global future_price
    df = pyupbit.get_ohlcv(ticker, interval='minute15', count=1000)


    future_price = 0
predict_price(ticker)

# predict future price every 15 minutes
schedule.every(15).minutes.do(lambda: predict_price(ticker))

# start auto trade
print("autotrade start!!")
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticker)
        end_time = start_time + datetime.timedelta(hours=12)
        schedule.run_pending()

        # 09:00 ~ 21:00
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            current_price = get_current_price(ticker)

            # if future price is higher than current price, buy the coin
            if future_price > current_price:
                krw = get_balance("KRW")
                if krw > 1000: # 최소 주문 가능 금액
                    buy_result = upbit.buy_marker_order(ticker, krw*0.9995) # 수수료 0.05%
                    post_message(myToken, "", "BTC buy: " + str(buy_result))

            # if future price is lower than current price, pass this time
            else:
                pass
            
            # selling time
            if now.minute % 15 == 0:
                btc = get_balance(tic)
                if btc > 0.00008:
                    sell_result = upbit.sell_market_order(ticker, btc*0.9995) # 수수료 0.05 고려
                    post_message(myToken, "", "BTC sell: " + str(sell_result))
        
        else:
            break
        
        # wait 1 minute
        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(myToken, "", e)
        time.sleep(1)

