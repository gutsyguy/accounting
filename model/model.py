import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras import Sequential
import numpy as np
import matplotlib.pyplot as plt

#import data
mnist = keras.datasets.mnist

#store data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

#Stores training data
X_train.shape

#Stores testing data
X_test.shape

#check minimum and maximum
np.min(X_train)
np.max(X_train)

#plot data
plt.figure()
plt.imshow(X_train[0])
plt.colorbar()

plt.figure()
plt.imshow(X_train[1])
plt.colorbar()

#allows for all 255 values to exists between 0 and 1
X_train = X_train/255.0
X_test = X_test/255.0
    
#Build model
model = Sequential()
model.add(Flatten(input_shape = (28, 28)))
model.add(Dense(128, activation = "relu"))
model.add(Dense(10, activation = 'softmax'))

#compile model
model.compile(optimizer = "adam", loss="sparse_categorical_crossentropy", metrics=['accuracy'])
model.fit(X_train, y_train, epochs = 10)

#checking loss and accuracy

test_loss, test_acc = model.evaluate(X_test, y_test)

#saving model
model.save("mnist_model.h5")

#load keras model
loaded_model = tf.keras.models.load_model("mnist_model.h5")

#convert to tflite
converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
tflite_model = converter.convert()

#save tflite model as a file

with open("mnist_model.tflite", "wb") as f:
    f.write(tflite_model)


print("Loss is "+ str(test_loss))
print("Accuracy is " + str(test_acc))