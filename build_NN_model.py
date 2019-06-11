import matplotlib.pyplot as plt
from keras.layers import Dense, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.utils import to_categorical

from load_NN import *

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
input_shape_original = X_train.shape[1]
# create model

model = Sequential()
model.add(Dense(300, input_dim=input_shape_original, activation='relu', kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(300, activation='relu' , kernel_initializer='normal'))
model.add(BatchNormalization())
model.add(Dropout(0.28))

model.add(Dense(37, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history=model.fit(X_train, y_train, epochs=250, batch_size=256,validation_split=0.2)
# serialize model to JSON
model.save('models/NN_Model_1.h5')
model_json = model.to_json()
with open("models/NN_Model_structure_1.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights('models/NN_Model_weights_1.h5')
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.ylim(0.4,1)
plt.savefig('model accuracy.jpg')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.ylim(0,1)
plt.savefig('model loss.jpg')
plt.show()
