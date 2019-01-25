
from segmentation import *
from matplotlib import pyplot as plt
import numpy as np
import cv2

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread('result_image/part102.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]

upgrade_image = cv2.imread('result_image/part102.jpg')

gray = cv2.cvtColor(upgrade_image, cv2.COLOR_BGR2GRAY)
upgrade_image = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
#contour_image,contour=contour_extraction(upgrade_image)
char_segmentation(image,upgrade_image,3)


