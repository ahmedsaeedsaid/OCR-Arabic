from scipy.io import loadmat
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import numpy as np

mat_data = loadmat('data/data_16.mat')
X=mat_data['X']
Y=mat_data['Y']
X_org=X.copy()
X = X.reshape((X.shape[0],(X.shape[1]*X.shape[2])))
X = X.astype(np.float64)
X = preprocessing.scale(X)
Y=Y.reshape((Y.shape[1],))
le = preprocessing.LabelEncoder()
le.fit(Y)
Y=le.transform(Y)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=42,stratify=Y)
