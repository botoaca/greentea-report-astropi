# note(@botoaca): This script is used to compute the percentage of vegetation in the images and save each percentage
#                 to a file. Since processing each image takes way too much, even when each dimension of the image
#                 is divided by 10, I decided to use multiprocessing in a pool of 12 logical processors (the amount
#                 my CPU has) to speed it up.

import os
import cv2
import time
import multiprocessing

__NDVI_PICS_FOLDER_PATH = "GREENTEA_DATA_NDVI/"
__OUTPUT_FILE_PATH = "vegetation_percentages.txt"

def pixel_is_greyscale(pixel):
    return pixel[0] == pixel[1] == pixel[2]

def compute_vegetation_percentage(image):
    image = cv2.resize(image, (image.shape[1], image.shape[0]))
    vegetation_pixels = sum([1 for row in image for pixel in row if not pixel_is_greyscale(pixel)])
    return vegetation_pixels / (image.shape[0] * image.shape[1]) * 100

def process_image(path):
    image = cv2.imread(__NDVI_PICS_FOLDER_PATH + path)
    percentage = compute_vegetation_percentage(image)
    return path, percentage

def main():
    if not os.path.isfile(__OUTPUT_FILE_PATH):
        open(__OUTPUT_FILE_PATH, "x")

    t_start = time.perf_counter()
    to_process = os.listdir(__NDVI_PICS_FOLDER_PATH)
    num_cpus = multiprocessing.cpu_count()
    with multiprocessing.Pool(num_cpus) as pool:
        percentages = pool.map(process_image, to_process)
    percentages = dict(percentages)
    t_end = time.perf_counter()

    with open(__OUTPUT_FILE_PATH, "w") as f:
        for key, value in percentages.items():
            f.write(f"{key}: {value}\n") 
        f.write(f"avg: {sum(percentages.values()) / len(percentages)}\n")
        f.write(f"time taken: {t_end - t_start} seconds")

if __name__ == "__main__":
    main()