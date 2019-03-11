from load_mat_file_NN import *
from keras.models import model_from_json
from keras.utils import to_categorical

# load json and create model

json_file = open('models/NN_Model_norm_3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("models/NN_Model_norm_3.h5")


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



