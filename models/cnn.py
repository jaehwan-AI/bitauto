from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D

def base(window_size, n_features):
    model = Sequential([
        Conv1D(filters=32, kernel_size=window_size, padding='causal', activation='relu', input_shape=[window_size, n_features]),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    return model
