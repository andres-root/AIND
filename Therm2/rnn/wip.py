import numpy as np


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

    print(X)
    print(y)

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


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


series = [1,3,5,7,9,11,13]
text = 'abcdefghijklmnopqrstuvwxyz'
window_size = 3
step_size = 2

# result = window_transform_series(series, window_size)
result = window_transform_text(text, window_size, step_size)
print(result)
