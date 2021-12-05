import cv2 
from time import sleep 

import urllib.request
import requests
import threading

from pyfirmata import Arduino
import pyfirmata

############################### Globals #############################################
counter = 0 
count_data = []
count_last = 0

in1 = 2
in2 = 4
in3 = 7
in4 = 12

ir1 = 8

a = ""


prowler_comms = Arduino("COM7")
prowler_comms.digital[ir1].mode = pyfirmata.INPUT
print("Started Firmata Comms... Version:",prowler_comms.get_firmata_version())

def fwd(prowler_comms:Arduino):
	prowler_comms.digital[in1].write(1)
	prowler_comms.digital[in2].write(0)
	prowler_comms.digital[in3].write(1)
	prowler_comms.digital[in4].write(0)
	prowler_comms.pass_time(1)

def bwd(prowler_comms:Arduino):
	prowler_comms.digital[in1].write(0)
	prowler_comms.digital[in2].write(1)
	prowler_comms.digital[in3].write(0)
	prowler_comms.digital[in4].write(1)
	prowler_comms.pass_time(1)

def idling(prowler_comms:Arduino):
	prowler_comms.digital[in1].write(0)
	prowler_comms.digital[in2].write(0)
	prowler_comms.digital[in3].write(0)
	prowler_comms.digital[in4].write(0)
	prowler_comms.pass_time(1)


def prowler_cloud_push():

	global counter

	#threading.Timer(60,prowler_cloud_push).start()   #looper

	URL = 'https://api.thingspeak.com/update?api_key='
	KEY = '23QZESQ05J54RCU6'
	HEADER = '&field1={}'.format(counter)
	new_URL = URL + KEY + HEADER

	pushed_url = urllib.request.urlopen(new_URL)
	print(pushed_url)
	

#######################################################################################
# Write api key =  23QZESQ05J54RCU6
# read api key =  8XU625IJNSHL5LHS
#######################################################################################



def start_vision():

	global counter, count_last, a

	cap_var = cv2.VideoCapture(0)


	core_detector = cv2.createBackgroundSubtractorMOG2(history = 100, varThreshold = 50)


	while True:

		ir_start()
		fwd(prowler_comms = prowler_comms)
		print(a)
		if (str(a) == "False"):

			break

		ret,frame = cap_var.read()

		#gettting our region of interest 
		height , width, _ = frame.shape
		# print(height,width)
		roi = frame[10:400, 400: 1000]

		# moving stuff becomes white 
		mask = core_detector.apply(roi)
		_, mask = cv2.threshold(mask , 254 , 255, cv2.THRESH_BINARY) # removing object shadows
		contours,_ = cv2.findContours(mask , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for cnt in contours:

			# finding the apt are and getting rid of anything
			# that is smaller than the box

			area = cv2.contourArea(cnt)
			if area > 42000: # 42k pixels

				x ,y, w ,h = cv2.boundingRect(cnt)
				cv2.rectangle(roi , (x,y), (x +w, y+h),(0,255,0),3)
				sleep(0.1)
				counter += 1
				# print(counter)

				count_data.append(counter)
				#cv2.drawContours(roi , [cnt], -1, (0,255,0), 2 )


		cv2.imshow("roi",roi)
		#cv2.imshow("Prowler Cam",frame)
		cv2.imshow("Mask", mask)


		key = cv2.waitKey(30)
		if key == 27:
			break
			# count_last =  count_data[-1]

	cap_var.release()
	cv2.destroyAllWindows()
	idling(prowler_comms = prowler_comms)

def ir_start():
	global a 

	it = pyfirmata.util.Iterator(prowler_comms)
	it.start()
	a = prowler_comms.digital[ir1].read()
	#print(a)

	return a	


if __name__ == '__main__':

	start_vision()
	idling(prowler_comms = prowler_comms)	
	print("Data pushed:",counter)
	prowler_cloud_push() # push the data

	
		

	

	 
	

	







