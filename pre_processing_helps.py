import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

def rotate_image(image):
    # convert the image to grayscale and flip the foreground
	# and background to ensure foreground is now "white" and
	# the background is "black"
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bitwise_not(gray)

	# threshold the image, setting all foreground pixels to
	# 255 and all background pixels to 0
	thresh = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# grab the (x, y) coordinates of all pixel values that
	# are greater than zero, then use these coordinates to
	# compute a rotated bounding box that contains all
	# coordinates
	coords = np.column_stack(np.where(thresh > 0))
	angle = cv2.minAreaRect(coords)[-1]

	# the `cv2.minAreaRect` function returns values in the
	# range [-90, 0); as the rectangle rotates clockwise the
	# returned angle trends to 0 -- in this special case we
	# need to add 90 degrees to the angle
	if angle < -45:
		angle = -(90 + angle)

	# otherwise, just take the inverse of the angle to make
	# it positive
	else:
		angle = -angle

	# rotate the image to deskew it
	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	return cv2.warpAffine(image, M, (w, h),
		flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

def remove_borders(cleaned_image,cleaned_image_inv):
	edges = cv2.Canny(cleaned_image_inv,50,150,apertureSize = 3)
	minLineLength = 100
	maxLineGap = 10
	lines = cv2.HoughLinesP(edges,1,np.pi/180,10,minLineLength,maxLineGap)
	if lines is None:
		return cleaned_image
	for line in lines:
		x1,y1,x2,y2 =line[0]
		cv2.line(cleaned_image,(x1,y1),(x2,y2),(0,0,0),2)
		cv2.line(cleaned_image_inv,(x1,y1),(x2,y2),(255,255,255),2)

	return  cleaned_image

def remove_watermark(img):
	alpha = 2.0
	beta = -160

	new = alpha * img + beta
	new = np.clip(new, 0, 255).astype(np.uint8)
	return new

