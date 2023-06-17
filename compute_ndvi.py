# note(@botoaca): This script computes the NDVI of the pictures in the GREEN_DATA_USEABLE folder, first by converting
#                 the image to grayscale, then by applying contrast stretching, then by computing the NDVI, then by
#                 applying contrast stretching again, as the picture becomes mostly black, then by applying the fastiecm
#                 colormap (from the Raspberry Pi Foundation's website) to the NDVI image, then by saving the image to
#                 the GREEN_DATA_NDVI folder.


import os
import cv2
import requests
import numpy as np

__USEABLE_PICS_FOLDER_PATH = "GREENTEA_DATA_USEABLE/"
__NDVI_PICS_FOLDER_PATH = "GREENTEA_DATA_NDVI/"
__ASTROPI_NDVI_FASTIECM_URL = "https://projects-static.raspberrypi.org/projects/astropi-ndvi/2cc9d1033d9c4f05388632e7912a4bb5531b3d94/en/images/fastiecm.py"

if not os.path.isfile("fastiecm.py"):
    open("fastiecm.py", "w").write(requests.get(__ASTROPI_NDVI_FASTIECM_URL).text)
from fastiecm import fastiecm

def contrast_stretch(image):
    in_min = np.percentile(image, 5)
    in_max = np.percentile(image, 95)
    out_min = 0.0
    out_max = 255.0
    out = image - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min
    return out

def compute_ndvi(image):
    b, _, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

def main():
    if not os.path.exists(__NDVI_PICS_FOLDER_PATH):
        os.mkdir(__NDVI_PICS_FOLDER_PATH)
    
    to_process = os.listdir(__USEABLE_PICS_FOLDER_PATH)
    for i in range(len(to_process)):
        image = cv2.imread(__USEABLE_PICS_FOLDER_PATH + to_process[i])
        contrasted = contrast_stretch(image)
        ndvi = compute_ndvi(contrasted)
        ndvi_contrasted = contrast_stretch(ndvi)
        color_mapped_prep = ndvi_contrasted.astype(np.uint8)
        color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
        cv2.imwrite(__NDVI_PICS_FOLDER_PATH + to_process[i], color_mapped_image)

if __name__ == "__main__":
    main()
