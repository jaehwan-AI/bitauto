import pyupbit

from datetime import datetime
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from dataset import cal_MA, bollinger, ATR
from dataset import MinMax, split_data, window_dataset
from models.base import base

from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

now = datetime.now()
save_path = '/media/nvidia/JetsonSSD-250/bit_data/'
ticker = "KRW-BTC"

# additional 지표
df = pyupbit.get_ohlcv(ticker, interval='minute30', count=1000)
df = cal_MA(df, days=5)
df = cal_MA(df, days=15)
df = bollinger(df, days=20, sigma=2)
df = ATR(df)

# processing missing data
df = df.dropna()

# Normalization
df = MinMax(df)

# split train & test set
x_train, x_test, y_train, y_test = split_data(df)

# dataset
window_size = 20
batch_size = 8
epochs = 50
train_data = window_dataset(x_train, y_train, window_size, batch_size, epochs, shuffle=True)
test_data = window_dataset(x_test, y_test, window_size, batch_size, epochs, shuffle=False)

# model
model = base(window_size=window_size, n_features=15)

loss = Huber()
optimizer = Adam(0.0005)
model.compile(loss=loss, optimizer=optimizer, metrics=['mse'])

earlystopping = EarlyStopping(monitor='loss', patience=10)
filename = os.path.join(save_path, 'checkpointer.ckpt')
checkpoint = ModelCheckpoint(filename, save_weights_only=True, save_best_only=True,
                             monitor='loss', verbose=1)

if len(x_train) % batch_size != 0:
    steps_per_epochs = len(x_train) // batch_size + 1
else:
    steps_per_epochs = len(x_train) // batch_size

if len(x_test) % batch_size != 0:
    valid_steps = len(x_test) // batch_size
else:
    valid_steps = len(x_test) // batch_size


print(len(x_train), len(x_test))
print(steps_per_epochs, valid_steps)
history = model.fit(train_data, verbose=1,# validation_data=test_data, verbose=0,
                    epochs=epochs, steps_per_epoch=steps_per_epochs, # validation_steps=valid_steps,
                    callbacks=[checkpoint, earlystopping])
# model evaluate steps=None
