from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras import optimizers
import pickle

from scipy.io import wavfile as wav
from scipy.fftpack import fft
from pathlib import Path
import numpy as np
import wave
import sys
import pickle

def tensorModel(output_neurons, output_activation_func, loss_calculator, trainFile):
	global x_train
	global y_train
	global x_test
	global y_test
	global x_individual
	neurons = 501
	activation_func = 'relu'

	model = Sequential()
	# Input layer
	model.add(Dense(neurons, kernel_initializer="uniform", input_dim=neurons, activation=activation_func))

	# First hidden layer
	model.add(Dense(neurons, kernel_initializer="uniform", activation=activation_func))

	model.add(Dense(neurons, kernel_initializer="uniform", activation=activation_func))
	model.add(Dropout(0.5))

	model.add(Dense(neurons, kernel_initializer="uniform", activation=activation_func))
	model.add(Dropout(0.2))

	# Output layer
	model.add(Dense(output_neurons, kernel_initializer="uniform", activation=output_activation_func))
	adam = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
	model.compile(loss=loss_calculator, optimizer=adam)

	model.fit(x_train, y_train, epochs=40, batch_size=5, validation_data=(x_test, y_test))
	score = model.evaluate(x_test, y_test, batch_size=1)
	print(score)
	for x_indi in x_individual:
		indiArray = [x_indi]
		print(model.predict(np.array(indiArray)))


typeMulti = True
if typeMulti:
	trainFile = 'store_1_multi_1'
else:
	trainFile = 'store_1_sigmoid_1'


f = open(trainFile + '.pckl', 'rb')
x_train, y_train, x_test, y_test = pickle.load(f)
f.close()

f = open('store_1_multi_test_1.pckl', 'rb')
x_individual, doncare = pickle.load(f)
f.close()

#f = open(trainFile + '_test_individual.pckl', 'rb')
#x_individual, s = pickle.load(f)
#f.close()


if typeMulti:
	tensorModel(2, 'softmax', 'categorical_crossentropy', trainFile)
else: 
	tensorModel(1, 'sigmoid', 'binary_crossentropy', trainFile)



