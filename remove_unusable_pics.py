# note(@botoaca): This script removes the pictures that are mostly black, as they are not usable.
#                 The way it decides is by converting it to grayscale to hold it's luminance, then
#                 resizing it to 8x8 pixels, then converting it to a list of pixels, then converting
#                 the pixels to 1s and 0s, where 1 is more black and 0 is more white, then summing
#                 the list and dividing it by the length of the list in order to get the average
#                 luminance of the picture. If the average luminance is greater than the threshold, which
#                 is 0.9 by default, then the picture is considered mostly black and is not copied over to
#                 the new GREEN_DATA_USEABLE folder.

from PIL import Image
import shutil
import os

__PICS_FOLDER_PATH = "GreenTea/GreenTea/GREENTEA_DATA/"
__USEABLE_PICS_FOLDER_PATH = "GREENTEA_DATA_USEABLE/"
__PICS_AMT = 1002
__PIC_TEMPLATE_NAME = "IMAGE_X.jpg"

def is_mostly_black(path, thresh=0.9):
    img = Image.open(path).convert("L").resize((8, 8)).getdata()
    img = [img[i] for i in range(len(img))]
    img = [1 if i < 128 else 0 for i in img]
    return sum(img) / len(img) >= thresh

def main():
    if not os.path.exists(__USEABLE_PICS_FOLDER_PATH):
        os.mkdir(__USEABLE_PICS_FOLDER_PATH)

    [
        shutil.copyfile(
            __PICS_FOLDER_PATH + __PIC_TEMPLATE_NAME.replace("X", str(i)),
            __USEABLE_PICS_FOLDER_PATH + __PIC_TEMPLATE_NAME.replace("X", str(i))
        )
        for i in range(__PICS_AMT)
        if not is_mostly_black(__PICS_FOLDER_PATH + __PIC_TEMPLATE_NAME.replace("X", str(i)))
    ]

if __name__ == "__main__":
    main()