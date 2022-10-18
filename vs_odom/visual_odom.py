
#from unittest import result
import cv2
import os
import image_similarity_measures.quality_metrics
import threading
from image_similarity_measures.quality_metrics import ssim, rmse,sre
from matplotlib import image
import rospy,threading
from sensor_msgs.msg import Image as ima
from cv_bridge import CvBridge
from nav_msgs.msg import Odometry
import csv, sys
from numba import jit, cuda
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped


class myThread (threading.Thread):
    def __init__(self, mat0, mat1):
        threading.Thread.__init__(self)
        self.mat0 = mat0
        self.mat1 = mat1
        self.ssim_value = 0.0
        self.rmse_value = 0.0
        self.sre_value = 0.0

    def run1(self):
       self.ssim_value=ssim(self.mat0, self.mat1)
       return self.ssim_value
    def run2(self):
       self.rmse_value=rmse(self.mat0, self.mat1)
       return self.rmse_value
    def run3 (self):
       self.sre_value= sre (self.mat0, self.mat1) 
       return self.ssim_value


class visual_odom(object):
	#@jit(target ="cuda")
	def __init__(self,which):
		if which == "map":
			self.ims = []
			self.file = open("dataset_test.csv","a+")
			self.ref = 0
			rospy.init_node('oodometry', anonymous=True,disable_signals=True)
			self.posit = rospy.Subscriber('odom',Odometry,self.odometryCb)
			self.imager = rospy.Subscriber("/camera/rgb/image_raw", ima, self.image_callback)
			self.data = {}
			rospy.spin()

		elif which == "nav":
			self.ims = []
			fo = open("dataset.csv","r")
			for k in fo.readlines()[1:]:
					
				self.ims.append(k.replace("\n","").split(",")[1])
					#print(k)
			fo.close()
			self.dax = self.chunker_list(self.ims,100)
				#self.file = open("dataset.csv","a+")
			self.ref = 0
			rospy.init_node('oodometry', anonymous=True,disable_signals=True)
			self.imager = rospy.Subscriber("/camera/rgb/image_raw", ima, self.image)
			self.data = {}
			rospy.spin()
			


	def odometryCb(self,msg):
			data_x = msg.pose.pose.position.x
			data_y = msg.pose.pose.position.y
			data_z = msg.pose.pose.position.z
			orie_x = msg.pose.pose.orientation.x
			orie_y = msg.pose.pose.orientation.y
			orie_z = msg.pose.pose.orientation.z
			orie_w = msg.pose.pose.orientation.w
			self.data = {"pos":{"x":data_x,"y":data_y,"z":data_y},"orie":{"x":orie_x,"y":orie_y,"z":orie_z,"w":orie_w}}
		
	def image_callback(self,msg):
			if msg.data and self.data != {}:
				bridge = CvBridge()
				cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
				pt = 'tmp_test/%s.jpeg'%self.ref
				cv2.imwrite(pt, cv2_img)
				self.file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(self.ref,pt,self.data["pos"]["x"],self.data["pos"]["y"],self.data["pos"]["z"],self.data["orie"]["x"],self.data["orie"]["y"],self.data["orie"]["z"],self.data["orie"]["w"]))
				self.ref =  self.ref + 1
				#self.imager.unregister()
	def chunker_list(self,seq, size):
			return(seq[i::size] for i in range(size))

	def calc_closest_val(self, lao, checkMax):
			result = {}
			if (checkMax):
				closest = max(lao.values())
				
			else:
				closest = min(lao.values())
			for key, value in lao.items():
				#print("The difference between ", key ," and the original image is : \n", value)
				if (value == closest):
					result[key] = closest
			#print("The closest value: ", closest)
			#print("######################################################################")
					
			return result
		#@jit(target ="cuda")
	def image(self,msg):
			if msg.data:
				bridge = CvBridge()
				test_img = bridge.imgmsg_to_cv2(msg, "bgr8")
				pt = 'test/current.jpeg'
				cv2.imwrite(pt, test_img)

				#test_img = img.data
				#test_img = cv2.imread('test/123.jpeg' )

				ssim_measures = {}
				rmse_measures = {}
				sre_measures = {}

				scale_percent = 100 # percent of original img size
				width = int(test_img.shape[1] * scale_percent / 100)
				height = int(test_img.shape[0] * scale_percent / 100)
				dim = (width, height)

				data_dir = 'tmp'
				for file in os.listdir(data_dir):
					#print("hello world!")
					img_path = os.path.join(data_dir, file)
					data_img = cv2.imread(img_path)
					resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
					
					th= myThread(test_img, resized_img)
					ssim_measures[img_path]= th.run1()
					rmse_measures[img_path]= th.run2()
					sre_measures[img_path]= th.run3()


				ssim = self.calc_closest_val(ssim_measures,True)
				rmse = self.calc_closest_val(rmse_measures, False)
				sre = self.calc_closest_val(sre_measures, True)
				#ssim = myThread(ssim_measures)
				#rmse = myThread(rmse_measures)
				#sre = myThread(sre_measures)



				print("The most similar according to SSIM: " , ssim)
				print("The most similar according to RMSE: " , rmse)
				print("The most similar according to SRE: " , sre)
				print(ssim.keys())
				image_ssim = list(ssim.keys())
				image_rmse = list(rmse.keys())
				image_sre = list(sre.keys())
				image_pose = ""
				if ((image_ssim[0] == image_rmse[0] or image_ssim[0] == image_sre[0]) and (image_rmse[0] != image_sre[0])) :
					image_pose = image_ssim[0]
				elif image_sre[0] == image_rmse[0] and (image_ssim[0] != image_rmse[0] and image_ssim[0] != image_sre[0]):
					image_pose = image_rmse[0]
				else :
					image_pose = image_rmse[0]
				print(image_pose)

				filename = 'dataset.csv'
				with open(filename, 'r') as f:
					reader = csv.reader(f)
					try:
						for row in reader:
							#print(row[1])
							
							if row[1]== image_pose:
							#if row[1]== "tmp1/0.jpeg":
								x= float(row[2])
								y= float(row[3])
								z=float(row[4])
								x_o=float(row[5])
								y_o=float(row[6])
								z_o=float(row[7])
								w_o=float(row[8])
								pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
								rospy.sleep(3)
								checkpoint = PoseWithCovarianceStamped()

								checkpoint.pose.pose.position.x = x
								checkpoint.pose.pose.position.y = y
								checkpoint.pose.pose.position.z = z

								#[x,y,z,w]=quaternion_from_euler(row[5],row[6],row[7])
								checkpoint.pose.pose.orientation.x = x_o
								checkpoint.pose.pose.orientation.y = y_o
								checkpoint.pose.pose.orientation.z = z_o
								checkpoint.pose.pose.orientation.w = w_o

								print (checkpoint)
								pub.publish(checkpoint)
								


					except csv.Error as e:
						sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
				


visual_odom("map")







