
#pip install python-chess

#!unzip stockfish.zip -d /content/stockfish

import chess
import chess.engine
import random
import numpy
import os
import subprocess
import tensorflow
import tensorflow.keras.callbacks as callbacks
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
from keras.models import load_model

STOCKFISHPATH = 'C:/Users/zihan/Desktop/School_Work/Game Design/MLchessAi/stockfish/stockfish-windows-x86-64-sse41-popcnt.exe'

#build model
def build_model(conv_size, conv_depth):
  board3d = layers.Input(shape=(14, 8, 8))

  x = board3d
  for _ in range(conv_depth):
      x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu')(x)
  x = layers.Flatten()(x)
  x = layers.Dense(64, 'relu')(x)
  x = layers.Dense(1, 'sigmoid')(x)

  return models.Model(inputs=board3d, outputs=x)

model = build_model(32, 4)
#utils.plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
#print(len(model.layers))

#Get the dataset from file
def get_dataset():
  container = numpy.load('eval1.npz')
  b, v = container['b'], container['v']
  v = v.astype(numpy.float32)
  v = numpy.asarray(numpy.round(v / abs(v).max() / 2 + 0.5, decimals=5), dtype=numpy.float64)
  return b, v

x_train, y_train = get_dataset()

#print(x_train.shape)
#print(y_train.shape)

model.compile(optimizer=optimizers.Adam(5e-4),loss='mean_squared_error')
model.summary()
model.fit(x_train, y_train,
          batch_size=256,
          epochs=100,
          verbose=1,
          validation_split=.1,
          callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                     callbacks.EarlyStopping(monitor='loss', patience=50, min_delta=0.1)])

model.save('eval1.keras')

