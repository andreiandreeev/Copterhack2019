from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30
cap = PiRGBArray(camera, size=(320, 240))

while(True):

	ret, frame = cap.read()

	gray_img 	   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, threshold_img = cv2.threshold(gray_img, 15, 255, cv2.THRESH_BINARY)

	cv2.imshow('Gray', gray_img)
	threshold2BGR_img  = cv2.cvtColor(threshold_img, cv2.COLOR_GRAY2BGR)

	height, width = threshold_img.shape
	roi_img   = threshold_img[0:height//2, 0:width//2]
	roi_left  = threshold_img[0:height//2, 0:width//4]
	roi_right = threshold_img[0:height//2, width//4:width//2]

	left_pxls  = cv2.countNonZero(roi_left)
	right_pxls = cv2.countNonZero(roi_right)

	print(left_pxls/right_pxls)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
cap.release()
