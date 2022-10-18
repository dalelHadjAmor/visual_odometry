from concurrent.futures import process
import cv2
import os
import image_similarity_measures
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import threading
import multiprocessing
#img = argv[0]

#test_img = cv2.imread('test/' + img)
test_img = cv2.imread('test/00.jpeg' )

ssim_measures = {}
rmse_measures = {}
sre_measures = {}

scale_percent = 100 # percent of original img size
width = int(test_img.shape[1] * scale_percent / 100)
height = int(test_img.shape[0] * scale_percent / 100)
dim = (width, height)

data_dir = 'tmp' 
threads1 = [10] 
threads2 = [10]
threads3 = [10]

for file in os.listdir(data_dir):
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    #for img_path in range(10):

    #ssim_measures[img_path]=  threading.Thread( target = ssim, args=( test_img, resized_img)).start()
    ssim_thread=  threading.Thread( target = ssim, args=( test_img, resized_img))       
    threads1.append(ssim_thread)
    #ssim_measures[img_path]= ssim_thread.start()
    
    print(type(ssim_measures[img_path]))
        #print("ok1")
    rmse_measures[img_path]= threading.Thread( target =rmse, args=(test_img, resized_img)).start()
    #threads2.append(rmse_measures[img_path])
        #print("ok2")
    sre_measures[img_path]= threading.Thread( target =sre, args=( test_img, resized_img)).start()
    #threads3.append(rmse_measures[img_path])
        #print("ok3")
        #print(n)
        #n+=1
    
"""""
    ssim_measures[img_path]=  ssim( test_img, resized_img)
        
      
        
    rmse_measures[img_path]= rmse( test_img, resized_img)
  
        
    sre_measures[img_path]= sre( test_img, resized_img)
"""""


def calc_closest_val(dict, checkMax):
    result = {}
    if (checkMax):
        closest = max(dict.values())
    else:
        closest = min(dict.values())
    		
    for key, value in dict.items():
        #print("The difference between ", key ," and the original image is : \n", value)
        if (value == closest):
            result[key] = closest
    #print("The closest value: ", closest)	    
    #print("######################################################################")
    return result
print(ssim_measures)   
#ssim = calc_closest_val(ssim_measures, True)
rmse = calc_closest_val(rmse_measures, False)
sre = calc_closest_val(sre_measures, True)


print("The most similar according to SSIM: " , ssim)
print("The most similar according to RMSE: " , rmse)
print("The most similar according to SRE: " , sre)