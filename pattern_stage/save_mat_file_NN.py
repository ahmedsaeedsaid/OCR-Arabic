import cv2
import numpy as np
import pandas as pd

characters_data = pd.read_csv('arabic.csv' )

X=[]
for url in characters_data['image']:
        image=cv2.imread(url,0)

        ret2,img_clean = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        image_resize=cv2.resize(img_clean,(16,16))
        X.append(image_resize)



X = np.array(X)
Y = characters_data['class'].values
#sio.savemat('data/data_16.mat', {'X':X,'Y':Y})

