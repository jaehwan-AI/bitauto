from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def base(window_size, n_features):
    model = Sequential([
        LSTM(32, activation='tanh', return_sequences=True),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    return model
