import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import math
import os

def file_extension(path):
    return os.path.splitext(path)[1]

def randomCrop(img) :
    x = random.randint(0, int(width*1/10))
    y = random.randint(0, int(height*1/10))
    w = width - int(width*1/10)
    h = height - int(height*1/10)
    croppedImg = img[y:y+h, x:x+w]
    croppedImg = cv2.resize(croppedImg, (width, height))
    return croppedImg

def borderLine(img):
    c = random.randint(0, 4)
    colors = [(0,0,0), (255,255,255), (255,0,0), (0,255,0), (0,0,255)]

    if random.randint(0, 1):
        for i in range(width):
            for color in range(3):
                img[0][i][color] = colors[c][color]

    if random.randint(0, 1):
        for i in range(width):
            for color in range(3):
                img[height-1][i][color] = colors[c][color]
    
    if random.randint(0, 1):
        for i in range(height):
            for color in range(3):
                img[i][0][color] = colors[c][color]

    if random.randint(0, 1):
        for i in range(height):
            for color in range(3):
                img[i][width-1][color] = colors[c][color]
    return img

def randomShifting(image):
    padding = random.randint(10, 25)
    oshape_h = height + (2 * padding)
    oshape_w = width + (2 * padding)
    img_pad = np.ones([oshape_h, oshape_w, depth], np.uint8) * 255
    img_pad[padding:padding+height, padding:padding+width, 0:depth] = image

    c = [0, padding*2]
    nh = c[random.randint(0, 1)]
    nw = c[random.randint(0, 1)]
    shiftedImg = img_pad[nh:nh + height, nw:nw + width]

    return shiftedImg

def reSize(img):
    p = random.randint(7,9)/10
    img = cv2.resize(img, (int(width*p), int(height*p)))
    top = random.randint(0, height-int(height*p))
    down = height-int(height*p) - top
    left = random.randint(0, width-int(width*p))
    right = width-int(width*p) - left
    imgPad = cv2.copyMakeBorder(img, top, down, left, right, cv2.BORDER_CONSTANT, value = (255,255,255))
    return imgPad

# Check if the folder is exits
folders = ["\\BorderLined", "\\Cropped", "\\Resized", "\\Shifted"]
for i in range(4):
    path = os.getcwd() + folders[i]
    if not os.path.isdir(path):
        os.mkdir(path)

path = os.getcwd() + '\\pictures'
if not os.path.isdir(path):
    print("There's no pictures folder!")
    exit(0)

for root, dirs, files in os.walk(path):
    for f in files:
        fullpath = os.path.join(root, f)
        if file_extension(fullpath) == '.jpg' or file_extension(fullpath) == '.png':
            imgOriginal = cv2.imread(fullpath)
            depth, width, height = imgOriginal.shape[::-1]
            cv2.imwrite(".\\Resized\\resized_" + f, reSize(imgOriginal))
            cv2.imwrite(".\\Shifted\\shifted_" + f, randomShifting(imgOriginal))
            cv2.imwrite(".\\BorderLined\\borderLined_" + f, borderLine(imgOriginal))
            cv2.imwrite(".\\Cropped\\cropped_" + f, randomCrop(imgOriginal))
