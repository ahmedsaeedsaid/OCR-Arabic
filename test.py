from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import pandas as pd
from segmentation import *
url='dataset/thaa/iAndalus_30 size5.jpg'
image=cv2.imread(url,0)

ret2,img_clean = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

img_clean = determination_image(img_clean)

cv2.imwrite('result_image/test.jpg',img_clean)
