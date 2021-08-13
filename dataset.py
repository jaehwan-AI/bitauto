import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def cal_MA(df, days):
    df[f'ma{days}'] = df['close'].rolling(days).mean()
    return df


def bollinger(df, days, sigma):
    df['bol_center'] = df['close'].rolling(days).mean() # center MA
    df['bol_ub'] = df['bol_center'] + sigma * df['close'].rolling(days).std() # upper band
    df['bol_lb'] = df['bol_center'] - sigma * df['close'].rolling(days).std() # lower band
    return df


def ATR(df):
    df['pclose'] = df['close'].shift(1)
    df['diff1'] = abs(df['high'] - df['low'])
    df['diff2'] = abs(df['pclose'] - df['high'])
    df['diff3'] = abs(df['pclose'] - df['low'])
    df['TR'] = df[['diff1', 'diff2', 'diff3']].max(axis=1)

    data = np.array(df['TR']) # no previous day's N
    for i in range(1, len(df)):
        data[i] = (19 * data[i-1] + df['TR'].iloc[i]) / 20
    df['ATR'] = data
    return df


def MinMax(df):
    scaler = MinMaxScaler()
    scale_cols = list(df.columns)
    scaled = scaler.fit_transform(df[scale_cols])
    dataframe = pd.DataFrame(scaled, columns=scale_cols)
    return dataframe


def split_data(df):
    x_train, x_test, y_train, y_test = train_test_split(df.drop('close', 1), df['close'],
                                                        test_size=0.1, random_state=0, shuffle=False)
    return x_train, x_test, y_train, y_test


def window_dataset(x, y, window_size, batch_size, epochs, shuffle):
    # feature window dataset
    ds_x = tf.data.Dataset.from_tensor_slices(x)
    ds_x = ds_x.window(window_size, shift=1, stride=1, drop_remainder=True)
    ds_x = ds_x.flat_map(lambda x: x.batch(window_size))

    # label window dataset
    ds_y = tf.data.Dataset.from_tensor_slices(y[window_size:])
    ds = tf.data.Dataset.zip((ds_x, ds_y))

    if shuffle:
        ds = ds.shuffle(len(x)-window_size)
        # return ds.repeat().batch(batch_size).prefetch(1)
    return ds.repeat(epochs).batch(batch_size).prefetch(1)


def split_stock(data, history_size, target_size, target_column):
    features = []
    labels = []

    for i in range(len(data)):
        x_end = i + history_size
        y_end = x_end + target_size
        if y_end > len(data):
            break
        tmp_x = data[i:x_end, :]
        tmp_y = data[x_end:y_end, target_column]
        features.append(tmp_x)
        labels.append(tmp_y)
    return np.array(features), np.array(labels)

