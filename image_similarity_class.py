from unittest import result
import cv2
import os
from cv2 import resize
import image_similarity_measures
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import threading
#img = argv[1]

test_img = cv2.imread('test/123.jpeg' )

ssim_measures = {}
rmse_measures = {}
sre_measures = {}

scale_percent = 100 # percent of original img size
width = int(test_img.shape[1] * scale_percent / 100)
height = int(test_img.shape[0] * scale_percent / 100)
dim = (width, height)

data_dir = 'tmp'

class myThread (threading.Thread):
	def __init__(self, lao):
		threading.Thread.__init__(self)
		self.loa = lao
	def run(self):
		calc_closest_val(self.loa)


#def resize_image(data_dir):

for file in os.listdir(data_dir):
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    ssim_measures[img_path]= ssim(test_img, resized_img)
    rmse_measures[img_path]= rmse(test_img, resized_img)
    sre_measures[img_path]= sre(test_img, resized_img)
    #return ssim_measures , rmse_measures, sre_measures 

def calc_closest_val(lao, checkMax):
    result = {}
    if (checkMax):
        closest = max(lao.values())
    else:
        closest = min(lao.values())
    		
    for key, value in lao.items():
       # print("The difference between ", key ," and the original image is : \n", value)
        if (value == closest):
            result[key] = closest
    	    
   # print("The closest value: ", closest)	    
   # print("######################################################################")
    return result


def image():
    ssim = calc_closest_val(ssim_measures, True)
    rmse = calc_closest_val(rmse_measures, False)
    sre = calc_closest_val(sre_measures, True)
   
    print("The most similar according to SSIM: " , ssim)
    print("The most similar according to RMSE: " , rmse)
    print("The most similar according to SRE: " , sre)


if __name__ == "__main__":
    image()
    '''
    ssim = calc_closest_val(ssim_measures, True)
    rmse = calc_closest_val(rmse_measures, False)
    sre = calc_closest_val(sre_measures, True)
    """"
    ssim = threading.Thread(target=calc_closest_val(ssim_measures,True),args=(1,))
    ssim.start()
    rmse = threading.Thread(target=calc_closest_val(rmse_measures,True),args=(1,))
    rmse.start()
    sre = threading.Thread(target=calc_closest_val(sre_measures,True),args=(1,))
    sre.start()"""
    print("The most similar according to SSIM: " , ssim)
    print("The most similar according to RMSE: " , rmse)
    print("The most similar according to SRE: " , sre)
'''































