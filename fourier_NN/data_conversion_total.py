import matplotlib.pyplot as plt
import matplotlib.axes as ax
from scipy.io import wavfile as wav
from scipy.fftpack import fft
from pathlib import Path
import numpy as np
import wave
import sys
import pickle

def convert_train_data(audioVowel):
	global fileName1
	global fileName2

	# Train Data
	print('Train data')
	temp_train = []
	list_train = []
	print('Steven train data')
	list_train, y_data = convert_train_data_from(fileName1, audioVowel, list_train)
	temp_train.extend(y_data)
	print('Matthijs train data')
	list_train, y_data = convert_train_data_from(fileName2, audioVowel, list_train)
	temp_train.extend(y_data)
	
	# Test data
	print('Test data')
	temp_train_test = []
	list_train_test = []
	list_train_test, y_data = convert_train_data_from(fileName1 + 'Test', audioVowel, list_train_test)
	temp_train_test.extend(y_data)

	list_train_test, y_data = convert_train_data_from(fileName2 + 'Test', audioVowel, list_train_test)
	temp_train_test.extend(y_data)

	return np.array(list_train), np.array(temp_train), np.array(list_train_test), np.array(temp_train_test)
	
def convert_train_data_from(audioFileName, vowel, data_list):
	global fileName2
	x = 1
	temp2_train = []
	while True:

		audiofile = '../AudioFiles/'+ str(vowel) + str(audioFileName) + str(x) + '.wav'
		if Path(audiofile).is_file():
			spf = wave.open(audiofile,'r')
		else: 
			break

		print(x)
		#Extract Raw Audio from Wav File
		signal = spf.readframes(-1)
		signal = np.fromstring(signal, 'Int16')
		fs = spf.getframerate()
		# Time and fft
		fft_out = fft(signal)
		Time=np.linspace(0, len(signal)/fs, num=len(signal))

		# Get corresponding y values
		xvalues = Time
		yvalues = np.abs(fft_out)

		goodvalues = int(181855 / 4)

		# Create new array for new graph of values
		yArrayValues = []
		for i in range(0, int(goodvalues*0.14), 8):
			idx = np.where(xvalues==xvalues[i])
			yArrayValues.extend(yvalues[idx]/(1* (10**7)))
			if i >= 3996:
				break

		z=0
		bigValue = 0
		zArrayValues = []
		for value in yArrayValues:
			bigValue += value
			if z == 10:
				zArrayValues.append(bigValue/10)
				bigValue = 0
				z = 0
			z += 1
		print(zArrayValues)
		xarray = range(len(zArrayValues))
		#plt.plot(xarray, yArrayValues)
		#plt.title(audiofile)
		data_list.append(zArrayValues)
		if typeMulti == True:
			if audioFileName == fileName2:
				temp2_train.append([1, 0])
			else:
				temp2_train.append([0, 1])
		else:
			if audioFileName == fileName2:
				temp2_train.append(1)
			else:
				temp2_train.append(0)
		x += 1
	return data_list, temp2_train
	

fileName1 = 'steven'
fileName2 = 'matthijs'
typeMulti = True
testFile = False

z = 1
if typeMulti:
	storeFile = 'multi_per10_'
	while True:
		if not Path(storeFile + str(z) + '.pckl').is_file():
			storeFile = storeFile + str(z)
			break
		z += 1


f = open(storeFile + '.pckl', 'wb')
pickle.dump(convert_train_data('E'), f)
f.close()


# Next 2 lines to show plot
# callFunc = convert_train_data('E')
# plt.show()