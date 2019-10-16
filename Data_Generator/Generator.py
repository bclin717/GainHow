import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

def randomCrop(img) :
    x = random.randint(0, int(width*2/3))
    y = random.randint(0, int(height*2/3))
    w = random.randint(100, width-200)
    h = random.randint(100, height-200)
    croppedImg = img[y:y+h, x:x+w]
    return croppedImg

def borderLine(img):
    for i in range(width):
        for color in range(3):
            img[0][i][color] = 0
            img[height-1][i][color] = 0
    
    for i in range(height):
        for color in range(3):
            img[i][0][color] = 0
            img[i][width-1][color] = 0
    return img

def randomShifting(image):
    padding = random.randint(1, 25)
    oshape_h = height + (2 * padding)
    oshape_w = width + (2 * padding)
    img_pad = np.zeros([oshape_h, oshape_w, depth], np.uint8)
    img_pad[padding:padding+height, padding:padding+width, 0:depth] = image

    c = [0, padding*2]
    nh = c[random.randint(0, 1)]
    nw = c[random.randint(0, 1)]
    shiftedImg = img_pad[nh:nh + height, nw:nw + width]

    return shiftedImg

def reSize(img):
    img = cv2.resize(img, (int(width*2/3), int(height*2/3)))
    return img

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCORR_NORMED']
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
def isSame(img, template):
    d, w, h = template.shape[::-1]
    img2 = img.copy()
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        try:
            res = cv2.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        except cv2.error:
            return False
        if (max_val < 0.5):
            return False



        print(min_val)
        print(max_val)
        
        
        if (min_val < 0.8 and max_val < 0.95):
            template = cv2.resize(template, (width, height))
            print("Resized:")
            try:
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            except cv2.error:
                return False
            if (max_val < 0.85 and min_val < 0.85):
                return False
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        cv2.imwrite(str(meth) + ".jpg", img)
    return True

imgOriginal = cv2.imread("EI6rDBqmt7BV61R-750x1125.jpg")
shape = imgOriginal.shape
height = shape[0]
width = shape[1]
depth = shape[2]

imgResized = reSize(imgOriginal)
imgShifted = randomShifting(imgOriginal)
imgBorderLined = borderLine(imgOriginal)
imgCropped = randomCrop(imgOriginal)

print(isSame(imgOriginal, imgResized))
print(isSame(imgOriginal, imgShifted))
print(isSame(imgOriginal, imgBorderLined))
print(isSame(imgOriginal, imgCropped))


img2 = cv2.imread("FullHD-Akira-Wallpaper.jpg")
img2 = cv2.resize(img2, (int(img2.shape[1]*1/3), int(img2.shape[0]*1/3)))

print(isSame(imgOriginal, img2))
