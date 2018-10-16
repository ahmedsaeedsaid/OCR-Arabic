'''
pre-processing stage
'''

from pre_processing_helps import *

image = cv2.imread('test_image/test_4.jpg')

rotated=rotate_image(image)
gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)

image_without_noise=cv2.fastNlMeansDenoising(gray,10,10,7,21)

image_without_noise = cv2.bitwise_not(image_without_noise)

# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
# link of threshold : https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html

img_clean = cv2.threshold(image_without_noise, 0, 255,cv2.THRESH_OTSU)[1]


#cv2.imwrite('result_image/Result_image_clean.jpg',img_clean)


