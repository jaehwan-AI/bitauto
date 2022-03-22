import datetime
import time

import pyupbit
import requests
import schedule
from fbprophet import Prophet

from inference import predict_arima, predict_prophet

# login
# access = "6zx2diWSu3Ad7I5z9maXjCYT7x5xZWGtnI4U3mtO"          # personal value
# secret = "e5Hp9qfxVCULo65ysIHxXFDy5ui9IEOxUCLSxK0j"          # personal value

# upbit = pyupbit.Upbit(access, secret)
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


future_price = 0
def predict_price(ticker):
    '''prediction future price'''
    global future_price
    df = pyupbit.get_ohlcv(ticker, interval='minute15', count=1000)
    df = df.reset_index()
    df['ds'] = df['index']
    df['y'] = df['close']
    data = df[['ds', 'y']]
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=)
    forecast = model.predict(future)
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace()]
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace()]
    closeValue = closeDf['yhat'].values[0]
    future_price = closeValue
predict_price(ticker)

# predict future price every 15 minutes
schedule.every(15).minutes.do(lambda: predict_price(ticker))

my_wallet = {"krw": 20000, "btc": 0}

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
                krw = my_wallet['krw']
                if krw > 1000: # 최소 주문 가능 금액
                    # btc = krw / current_price
                    my_wallet['btc'] = (krw*0.9995) / current_price # 수수료 0.05%
                    post_message(myToken, "", "BTC buy: " + str(my_wallet['btc']))

            # if future price is lower than current price, pass this time
            else:
                pass
            
            # selling time
            if now.minute % 15 == 0:
                btc = my_wallet['btc']
                if btc > 0.00001:
                    # krw = btc * current_price
                    my_wallet['krw'] = (btc*0.9995) * current_price # 수수료 0.05 고려
                    post_message(myToken, "", "BTC sell: " + str(my_wallet['krw']))
        else:
            break
        
        # wait 1 minute
        time.sleep(1)

    except Exception as e:
        print(e)
        post_message(myToken, "", e)
        time.sleep(1)

