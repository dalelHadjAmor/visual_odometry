import cv2
import os
import image_similarity_measures
from sys import argv
from image_similarity_measures.quality_metrics import rmse, ssim, sre
from multiprocessing import Pool
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
   
for file in os.listdir(data_dir):
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    with Pool(processes=3) as pool:
        #ssim_measures[img_path]= pool.apply_async(ssim, test_img, resized_img)
        proc= pool.apply_async(ssim, test_img, resized_img)
        rmse_measures[img_path]= pool.apply_async(rmse, test_img, resized_img)
        sre_measures[img_path]= pool.apply_async(sre, test_img, resized_img)

print(proc)
"""""
def calc_closest_val(dict, checkMax):
    result = {}
    if (checkMax):
        closest = max(dict.values())
    else:
        closest = min(dict.values())
    		
    for key, value in dict.items():
        print("The difference between ", key ," and the original image is : \n", value)
        if (value == closest):
            result[key] = closest
    print("The closest value: ", closest)	    
    print("######################################################################")
    #print(ssim_measures[img_path])
    return result
print(ssim_measures)
ssim = calc_closest_val(ssim_measures, True)
rmse = calc_closest_val(rmse_measures, False)
sre = calc_closest_val(sre_measures, True)



print("The most similar according to SSIM: " , ssim)
print("The most similar according to RMSE: " , rmse)
print("The most similar according to SRE: " , sre)"""