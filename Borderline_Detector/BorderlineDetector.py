from cv2 import *
import numpy as np
from os import walk
from os.path import join
import os

def file_extension(path):
    return os.path.splitext(path)[1]

def isComp(path):
    s = os.path.splitext(path)[0]
    if s[-4:] == "comp":
        return True
    return False

def display(windowName, img):
    namedWindow(windowName, WINDOW_NORMAL)
    resizeWindow(windowName, 700, 1000)
    imshow(windowName, img)

def checkX(img, height):
    start = int(height*0.3)
    end = int(height*0.7)
    
    value = int(img[0][start])
    for i in range(start, end):
        if (img[0][i] >= value+10) or (img[0][i] <= value-10):
            return False
    return True
        
def checkY(img, width):
    start = int(width*0.3)
    end = int(width*0.7)
    
    value = img[start][0]
    for i in range(start, end):
        if (img[i][0] >= value+10) or (img[i][0] <= value-10):
            return False
    return True

def checkMiddleY(img, width, height):
    middle = int(height/2)
    value = int(img[0][middle]/10)
    for i in range(0, 30):
        if int(img[i][middle]/10) != value:
            return True
    return False

def checkMiddleX(img, width, height):
    middle = int(width/2)
    value = int(img[middle][0]/10)
    for i in range(0, 30):
        if int(img[middle][i]/10) != value:
            return True
    return False

def check(f):
    global img_original
    img_original = imread(str(f))
    img = cvtColor(img_original, COLOR_BGR2GRAY)
    width = img.shape[0]
    height = img.shape[1]

    if (checkY(img, width) and checkMiddleX(img, width, height)) or (checkX(img, height) and checkMiddleY(img, width, height)):
        return True


# e.g. CFU_WE_0917/0917-1/E
mypath = os.getcwd()
global img_original
fp = open("Output.txt", "w")
for root, dirs, files in walk(mypath):
    for f in files:
        fullpath = join(root, f)
        if isComp(fullpath):
            continue
        if file_extension(fullpath) == ".jpg":
            print(fullpath)
            if check(fullpath):
                # imwrite("./" + str(f), img_original)
                fp.write(fullpath + "\n")
fp.close()

