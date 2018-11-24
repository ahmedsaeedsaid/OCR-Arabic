'''
pre-processing stage
'''

from pre_processing_helps import *

image = cv2.imread('test_image/test_13.jpg')

#image = remove_watermark(image)

#rotated=rotate_image(image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image_without_noise=cv2.fastNlMeansDenoising(gray,10,10,7,21)

# threshold the image, setting all foreground pixels to
# 255 and all background pixels to 0
# link of threshold : https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html

img_clean = cv2.adaptiveThreshold(image_without_noise,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,9,2)
#img_clean_inv = cv2.adaptiveThreshold(image_without_noise,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)

#img_clean=remove_borders(img_clean,img_clean_inv)
cv2.imwrite('result_image/Result_image_clean.jpg',img_clean)
