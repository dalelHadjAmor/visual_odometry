from concurrent.futures import thread
import cv2
import os
import image_similarity_measures
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
from multiprocessing import Pool , Manager
import threading
import multiprocessing


#img = argv[0]


class myThread (threading.Thread):
    def __init__(self, mat0, mat1):
        threading.Thread.__init__(self,)
        
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



def calc_closest_val(  dic, checkMax):
			result = {}

			if (checkMax):
				closest = max(dic.values())
				
			else:
				closest = min(dic.values())
			for key, value in dic.items():
				#print("The difference between ", key ," and the original image is : \n", value)
				if (value == closest):
					result[key] = closest
			#print("The closest value: ", closest)
			#print("######################################################################")
					
			return result



#test_img = cv2.imread('test/' + img)
test_img = cv2.imread('test/00.jpeg' )
print("ok")
manager = Manager()
#ssim_measures = manager.dict()
#rmse_measures = manager.dict()
#sre_measures = manager.dict()
ssim_ = manager.dict()
rmse_ = manager.dict()
sre_ = manager.dict()
ssim_measures = {}
rmse_measures = {}
sre_measures = {}

scale_percent = 100 # percent of original img size
width = int(test_img.shape[1] * scale_percent / 100)
height = int(test_img.shape[0] * scale_percent / 100)
dim = (width, height)

data_dir = 'tmp' 

print("hi")
#threads = []
for file in os.listdir(data_dir):
    
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    #ssim_measures[img_path]= ssim( test_img, resized_img)
    #rmse_measures[img_path]= rmse( test_img, resized_img)
    #sre_measures[img_path]= sre( test_img, resized_img)
    #ssim_measures = multiprocessing.Process(target=ssim, args=( test_img, resized_img))
    #ssim_measures .start()
    #for k in range(10):
    #threads = []
    #for t in range (5):
    #threads.append(myThread( test_img, resized_img))
    #for th in threads:
        
    th= myThread(test_img, resized_img)

    ssim_measures[img_path]= th.run1()
    rmse_measures[img_path]= th.run2()
    sre_measures[img_path]= th.run3()
        
    print("ssim_measures[img_path]= ", ssim_measures[img_path])
    print("rmse_measures[img_path]= ", rmse_measures[img_path])
    print("sre_measures[img_path]= ", sre_measures[img_path])
   
print(ssim_measures)
print(rmse_measures)
print(sre_measures)
#print(rmse_measures)
#print(sre_measures)
ssim = calc_closest_val(ssim_measures,True)
rmse = calc_closest_val(rmse_measures, False)
sre = calc_closest_val(sre_measures, True)





print("ssim= ", ssim)
print("rmse=" , rmse)
print("sre=", sre)


