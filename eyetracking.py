import cv2
def nothing(x):
    pass

drawing      = False
roi_selected = False

roi_lefttop  = ()
roi_rightbot = ()

cap = cv2.VideoCapture('test1.mp4')

cv2.namedWindow('Threshold')
cv2.createTrackbar('Threshold', 'Threshold', 128, 255, nothing)
cv2.createTrackbar('Left', 'Threshold', 0, 120, nothing)
cv2.createTrackbar('Right', 'Threshold', 60, 250, nothing)

def select_roi(event, x, y, flags, param):
	global roi_lefttop, roi_rightbot, drawing, roi_selected

	if event == cv2.EVENT_LBUTTONDOWN:
		if roi_selected == False:
			if drawing == False:
				drawing = True
				roi_lefttop = (x,y)
			else:
				drawing = False
				roi_selected = True

	elif event == cv2.EVENT_MOUSEMOVE:
		if drawing == True:
			roi_rightbot = (x,y)



cv2.setMouseCallback("Threshold", select_roi)

while(True):

	ret, frame = cap.read()

	gray_img 	   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret, threshold_img = cv2.threshold(gray_img, cv2.getTrackbarPos('Threshold', 'Threshold'), 255, cv2.THRESH_BINARY)

	cv2.imshow('Gray', gray_img)
	threshold2BGR_img  = cv2.cvtColor(threshold_img, cv2.COLOR_GRAY2BGR)

	if roi_lefttop:
		if roi_rightbot:
			cv2.rectangle(threshold2BGR_img, roi_lefttop, roi_rightbot, (0,0,255), 1)

	cv2.imshow('Threshold', threshold2BGR_img)

	if roi_selected:
		roi_img   = threshold_img[roi_lefttop[1]+1:roi_rightbot[1], roi_lefttop[0]+1:roi_rightbot[0]]
		roi_left  = threshold_img[roi_lefttop[1]+1:roi_rightbot[1], roi_lefttop[0]+1:(roi_rightbot[0]+roi_lefttop[0]+1)//2]
		roi_right = threshold_img[roi_lefttop[1]+1:roi_rightbot[1], (roi_rightbot[0]+roi_lefttop[0]+1)//2:roi_rightbot[0]]

		left_pxls  = cv2.countNonZero(roi_left)
		right_pxls = cv2.countNonZero(roi_right)

		cv2.imshow('LeftRoi', roi_left)
		cv2.imshow('RightRoi', roi_right)
		cv2.imshow('ROI', roi_img)
		print(roi_lefttop, roi_rightbot)
		if left_pxls != 0:
			if right_pxls/left_pxls < cv2.getTrackbarPos('Left', 'Threshold')/100:
				print("Left")
			elif right_pxls/left_pxls > cv2.getTrackbarPos('Right', 'Threshold')/100:
				print("Right")
			else:
				print("Forward")

	if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
cap.release()
cv2.destroyAllWindows()
sock.close()
