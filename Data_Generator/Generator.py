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

def bloodBorderLine(img):
    loc = 28
    thickness = 4
    colors = [0,0,255]
    
    for x in range(loc, loc+thickness):
        for i in range(x, width-x):
            for color in range(3):
                img[x][i][color] = colors[color]
                img[height-x][i][color] = colors[color]
                
        for i in range(x, height-x):
            for color in range(3):
                img[i][x][color] = colors[color]
                img[i][width-x][color] = colors[color]

    return img

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

def drawline(img, pt1=(0,0), pt2=(0,0), color=(0,0,255), thickness=0, gap=0) :
    imgLine = img.copy()
    if pt1==(0,0) and pt2==(0,0):
        pt1 = (random.randint(10, width-10), random.randint(10, int(height/2)))
        pt2 = (random.randint(10, width-10), random.randint(pt1[1], height))

    if thickness==0 and gap==0:
        thickness = random.randint(1, 5)    
        gap = random.randint(5, 25)


    cv2.line(imgLine, pt1, pt2, color, thickness)

    dist = ((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in np.arange(0, dist, gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)
    
    count = 0
    for p in pts:
        if(count % 2 == 0):
            p1 = p
        else:
            p2 = p
            cv2.line(img, p1, p2, color, thickness)
        count += 1

    return img, imgLine

# Check if the folder is exits
folders = ["\\BorderLined", "\\Cropped", "\\Resized", "\\Shifted", "\\Blooded", "\\DashedLine", "\\Line"]
for i in range(len(folders)):
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
            # cv2.imwrite(".\\Resized\\resized_" + f, reSize(imgOriginal))
            # cv2.imwrite(".\\Shifted\\shifted_" + f, randomShifting(imgOriginal))
            # cv2.imwrite(".\\BorderLined\\borderLined_" + f, borderLine(imgOriginal))
            # cv2.imwrite(".\\Cropped\\cropped_" + f, randomCrop(imgOriginal))
            # cv2.imwrite(".\\Blooded\\blooded_" + f, bloodBorderLine(imgOriginal))
            dashedLine, Line = drawline(imgOriginal, (0, 0), (0, 0), (0, 0, 255), 0, 0)
            cv2.imwrite(".\\DashedLine\\dashedLine_" + f, dashedLine)
            cv2.imwrite(".\\Line\\Line_" + f, Line)