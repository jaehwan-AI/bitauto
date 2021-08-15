# import pyupbit

# from datetime import datetime
# import numpy as np
# import pandas as pd
# # import tensorflow as tf
# from dataset import split_stock

# now = datetime.now()
# ticker = "KRW-BTC"

# df = pyupbit.get_ohlcv(ticker=ticker, interval='minute5', count=1000)

# # ATR in turtle trading
# df['pclose'] = df['close'].shift(1)
# df['diff1'] = abs(df['high'] - df['low'])
# df['diff2'] = abs(df['pclose'] - df['high'])
# df['diff3'] = abs(df['pclose'] - df['low'])
# df['TR'] = df[['diff1', 'diff2', 'diff3']].max(axis=1)

# data = np.array(df['TR']) # no previous day's N
# for i in range(1, len(df)):
#     data[i] = (19 * data[i-1] + df['TR'].iloc[i]) / 20

# df['ATR'] = data

# # bollinger_band
# d = 20
# sigma = 2
# df['bol_center'] = df['close'].rolling(d).mean() # center MA
# df['bol_ub'] = df['bol_center'] + sigma * df['close'].rolling(d).std() # upper band
# df['bol_lb'] = df['bol_center'] - sigma * df['close'].rolling(d).std() # lower band

# # moving average
# df['ma5'] = df['close'].rolling(5).mean()
# df['ma15'] = df['close'].rolling(15).mean()

# print(df.head())
# print(df.tail())

import pyupbit
from datetime import datetime
import os

from dataset import cal_MA, bollinger, ATR
from dataset import MinMax, split_data, window_dataset
from models.base import base

from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

now = datetime.now()
save_path = '/media/nvidia/JetsonSSD-250/bit_data/'
ticker = "KRW-BTC"

df = pyupbit.get_ohlcv(ticker, interval='minute30', count=1000, period=1)
df = cal_MA(df, days=5)
df = cal_MA(df, days=15)
df = bollinger(df, days=20, sigma=2)
df = ATR(df)

df = df.dropna()
df = MinMax(df)

x_train, x_test, y_train, y_test = split_data(df)

window_size = 20
batch_size = 8
epochs = 5
train_data = window_dataset(x_train, y_train, window_size, batch_size, epochs, shuffle=True)
test_data = window_dataset(x_test, y_test, window_size, batch_size, epochs, shuffle=False)

# model = base(window_size=window_size, n_features=16)

# loss = Huber()
# optimizer = Adam(0.0005)
# model.compile(loss=loss, optimizer=optimizer, metrics=['mse'])

# earlystopping = EarlyStopping(monitor='loss', patience=3)
# filename = os.path.join(save_path, 'checkpointer.ckpt')
# checkpoint = ModelCheckpoint(filename, save_weights_only=True, save_best_only=True,
#                              monitor='loss', verbose=1)

# if len(x_train) % batch_size != 0:
#     steps_per_epochs = len(x_train) // batch_size + 1
# else:
#     steps_per_epochs = len(x_train) // batch_size

# if len(x_test) % batch_size != 0:
#     valid_steps = len(x_test) // batch_size
# else:
#     valid_steps = len(x_test) // batch_size

# print(len(x_train), len(x_test))
# print(steps_per_epochs, valid_steps)

# history = model.fit(train_data, verbose=1,# validation_data=test_data, verbose=0,
#                     epochs=epochs, steps_per_epoch=steps_per_epochs, # validation_steps=valid_steps,
#                     callbacks=[checkpoint, earlystopping])

# y_hat = model.predict(test_data)
# print(y_hat)

