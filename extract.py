import glob, os
from scipy.io import loadmat
import numpy as np
import cv2

outputfolder = "Results"


if not os.path.exists(outputfolder):
	os.makedirs(outputfolder)

files = glob.glob("*.png")
count = 0
for file in files:
    x = loadmat(file[:-4] + "_objects.mat")
    item = (x['objects']['ordering'])
    name = (x['objects']['name'].item())
    arr1 = []
    for nm in name:
        for n in nm:
            arr1.append(n[0])

    for it in item:
        for i in it:
            try: 
                i = i[0]
#                print i
                dictionary = dict(zip(arr1, i))
#                print dictionary
                for key in dictionary:
                    fpath = outputfolder + '/' + key
                    if not os.path.exists(fpath):
                        os.makedirs(fpath)
##                    os.mkdir(key)
                    t = x["objects"]["labels"][0][0]
                    S = np.where(t == dictionary[key])
#                    print S
                    minx = min(S[0])
                    maxx = max(S[0])
                    miny = min(S[1])
                    maxy = max(S[1])
                    img = cv2.imread(file)
                    crop_img = img[minx:maxx, miny:maxy]
                    path = fpath + "/Img_" + str(count) + ".png"
#                    print path
                    cv2.imwrite(path, crop_img)
                    count += 1
            except:
                print file + " has no labels"
                pass
