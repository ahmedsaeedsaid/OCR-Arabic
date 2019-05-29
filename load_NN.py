from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
from segmentation import *

characters_data = pd.read_csv('arabic.csv')
X=[]
for url in characters_data['image']:
        image=cv2.imread(url,0)
        ret2,img_clean = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        img_clean = determination_image(img_clean)
        image_resize=cv2.resize(img_clean,(16,16))
        X.append(image_resize)

X = np.array(X)
Y = characters_data['class'].values
X = X.reshape((X.shape[0],(X.shape[1]*X.shape[2])))
X = X.astype(np.float64)
le = preprocessing.LabelEncoder()
le.fit(Y)
Y=le.transform(Y)

X/=255
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state=42,stratify=Y)


