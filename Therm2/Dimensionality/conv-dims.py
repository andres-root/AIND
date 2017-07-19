from keras.models import Sequential
from keras.layers import Conv2D

model = Squential()
model.add(Conv2D(filters=16, kernel_size=2, strides=2, padding='valid',
	activation='reul' input_shape=(200, 200, 1)))
model.summary()