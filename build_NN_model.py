from keras.models import Sequential
from keras.layers import Dense, Dropout,regularizers
from keras.utils import to_categorical
from load_mat_file_NN import *
import matplotlib.pyplot as plt
from keras.layers.normalization import BatchNormalization

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

model.add(Dense(32, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history=model.fit(X_train, y_train, epochs=200, batch_size=256,validation_split=0.25)
# serialize model to JSON
model_json = model.to_json()
with open("models/NN_Model_norm_3.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights('models/NN_Model_norm_3.h5')
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.ylim(0.8,1)
plt.savefig('model accuracy.jpg')
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.ylim(0,0.4)
plt.savefig('model loss.jpg')
