import cv2
import numpy as np
import time

print "This is a game to clean the windows."
print "Score is calculated with respect to cleaning progress made with each frame"
print 
print "Enter Your Options for camera: "
print "1) 1 for internal webcamera"
print "2) 2 for external webcamera"

z = int(raw_input())

print "Enter Your Options to clean: "
print "1) 1 for hands"
print "2) 2 for green color object"
print "3) 3 for yellow color object"

z1 = int(raw_input())

if z1 == 2:
	#### Masking Value for Green block
	param1 = [50,160,0]
	param2 = [120,255,70]

elif z1 == 3:
	##### Masking Value for Yellow Block
	param1 = [80,200,200]
	param2 = [180,255,255]

else:
	# ##### Masking Vlaue for Hand
	param1 = [60,100,150]
	param2 = [130,155,230]

cap =cv2.VideoCapture(z-1)									# change 0 to 1 if you want to use external webcam
counter = 0
score = 0

for i in range(1,4):      									# Working for 3 levels of the game
	
	flag = 0
	img = cv2.imread("images/haze"+str(i)+".jpg")			# Reading the that will casue dirt on teh frame
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)				
	frame1 = cv2.imread("images/frame"+str(i)+".jpg")		# Reading the frame(outer boundary of the resultant image)
	
	z = 305
	z1 = 30
	previous_len = 1
	previous_len1 = 1
	previous_area = 0
	
	while(1):

		ret,frame = cap.read()

######## STAGE 1: Masking Image for the pixels with colour values of hand #############		
		
		lower = np.array(param1)
		upper = np.array(param2)
		mask = cv2.inRange(frame, lower, upper)
		ret,thresh = cv2.threshold(mask,5,255,cv2.THRESH_BINARY_INV)
		
######## Stage 2: Performing Bitwise operations to overlay images and creating hazy effects ######### 
		img = cv2.bitwise_and(thresh, img)			
		mask = cv2.inRange(img, 0, 5)
		thresh = cv2.bitwise_or(mask, img)
		thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
		thresh = cv2.bitwise_and(frame, thresh)
		
		thresh = cv2.flip(thresh, 2)    ######  Flip operation to nullify inversion due to webcam

################################ CLOCK PORTION ##############################################
		
		cv2.rectangle(thresh,(275,5),(375,55),(0,0,0),-1)
		cv2.rectangle(thresh,(280,10),(370,50),(0,255,255),-1)
		
		if len(str(int(time.clock()))) > previous_len:
			z = z - 10
			previous_len = previous_len+1
		cv2.putText(thresh, str(int(time.clock())/60) +':'+ str(int(time.clock()) % 60) , (z,40), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)


################################ PERCENTAGE PORTION #########################################
		
		cv2.rectangle(thresh,(5,5),(105,55),(0,0,0),-1)
		cv2.rectangle(thresh,(10,10),(100,50),(0,255,255),-1)
		
		area = 0
		ret,img_per = cv2.threshold(mask,5,255,cv2.THRESH_BINARY_INV)
		contours, hierarchy = cv2.findContours(img_per,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

		for c in range(1,len(contours)):
			area = area + cv2.contourArea(contours[c])
		
####### STAGE 3: Calculation of score ########################################################		
		
		diff_area = previous_area - area
		previous_area = area	

		if diff_area > 0:
			score = score + diff_area

##############################################################################################

		if area != 0:
			counter = 1
			if len(str(int(((303849 - area)/303849) * 100))) > previous_len1:
				z1 = z1 - 10
				previous_len1 = previous_len1+1

			percentage = int(((303849 - area)/303849) * 100)
			cv2.putText(thresh, str(int(((303849 - area)/303849) * 100)) + '%' , (z1,40), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

		else:
			percentage = 0
			cv2.putText(thresh,  '0%' , (z1,40), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
			if counter == 1:
				flag = 1

		frame1[50:530,50:690] = thresh 

#################################### Printing Final Score ###################################### 
		
		if i == 3 and flag == 1:
			cv2.putText(frame1,'Your Score' , (200,200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), 10)
			cv2.putText(frame1, str(int((950000 - score)/100)) + "/ 9500", (170,300), cv2.FONT_HERSHEY_SIMPLEX, 2, (127,0,255), 10)

		cv2.putText(frame1, "Press ESC to close window" , (150,570), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)
		cv2.putText(frame1, "STAGE "+str(i) , (250,40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 5)
		
		#cv2.imshow('img',img)					# Display Image to show cleaned area
		cv2.imshow('thresh',frame1)
		
		if cv2.waitKey(1) == 27 or (flag == 1 and i!=3):
			break

cv2.waitKey(0)
cv2.destroyAllWindows()