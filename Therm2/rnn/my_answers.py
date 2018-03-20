import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []
    for i in range(len(series)):
        fi = i + (window_size)
        if fi  <= (len(series) - 1):
            window = series[i:fi]
            X.append(window)
            y.append(series[fi])

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape=(window_size, 1), activation='tanh'))
    model.add(Dense(1, input_shape=(window_size, 1)))
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    allowed = ['a','b','c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u', 'v', 'w', 'x', 'y', 'z',' ', '!', ',', '.', ':', ';', '?']
    text = [c for c in text if c in allowed]

    return ''.join(text)

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    current_step = 1

    for i in range(len(text)):
        if current_step == step_size or i == 0:
            fi = i + (window_size)
            if fi  <= (len(text) - 1):
                window = text[i:fi]
                inputs.append(window)
                outputs.append(text[fi])
            current_step = 1
        else:
            current_step += 1

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars), activation='tanh'))
    model.add(Dense(num_chars, activation='linear'))
    model.add(Dense(num_chars, activation='softmax'))

    return model
