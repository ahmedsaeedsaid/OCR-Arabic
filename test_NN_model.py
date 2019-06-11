from keras.models import load_model
from keras.utils import to_categorical
#from load_NN import *
import numpy as np
import matplotlib.pyplot as plt

# load model
loaded_model=load_model('models/NN_Model_1.h5')

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

men_means, men_std = (99.54, 99.55, 99.43), (1, 1, 1)

ind = np.arange(len(men_means))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind ,men_means, width, yerr=men_std , color='green')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by scope of data')
ax.set_xticks(ind)
ax.set_xticklabels(('all data', 'train data', 'test data'))
ax.legend()


def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


autolabel(rects1, "center")
plt.savefig('acc.jpg')



'''
print('accuracy::', metrics.accuracy_score(y, y_pred))
print('precision::', metrics.precision_score(y, y_pred, average='weighted'))
print('recall::', metrics.recall_score(y, y_pred, average='weighted'))
print('f_score::', metrics.f1_score(y, y_pred, average='weighted'))
print('f_score::', metrics.classification_report(y, y_pred))
'''
