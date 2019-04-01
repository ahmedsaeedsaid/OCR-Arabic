from keras.models import load_model
from keras.utils import to_categorical

from load_mat_file_NN import *

# load model
loaded_model=load_model('models/NN_Model_norm.h5')

y_test = to_categorical(y_test)
y_train = to_categorical(y_train)
Y = to_categorical(Y)


# evaluate loaded model on test data
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
score1 = loaded_model.evaluate(X_test, y_test)
score2 = loaded_model.evaluate(X_train, y_train)
score3 = loaded_model.evaluate(X, Y)


print("all  data %s: %.2f%%" % (loaded_model.metrics_names[1], score3[1]*100))
print("train data %s: %.2f%%" % (loaded_model.metrics_names[1], score2[1]*100))
print("test data %s: %.2f%%" % (loaded_model.metrics_names[1], score1[1]*100))



