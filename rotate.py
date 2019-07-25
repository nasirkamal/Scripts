import cv2
import os
import glob
import numpy as np
from scipy import ndimage

images_from = 'C:/Users/Nasir_kamal/Documents/Cookies/RIO/Images'
images_to = 'C:/Users/Nasir_kamal/Documents/Cookies/RIO/Scaled'
angle = 90
ext = '.jpg'

try:
	os.mkdir(images_to)
except:
	print('Warning: ' + images_to +' directory already exists')

file_list = sorted(glob.glob(images_from + '/*' + ext))

for idx,file_name in enumerate(file_list):
	f_name = file_name.split('\\')[-1]
	img = cv2.imread(file_name)
	rotated = ndimage.rotate(img, angle)
	cv2.imwrite(images_to + '/' + f_name, rotated)
