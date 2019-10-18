import cv2
import numpy as np

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCORR_NORMED']
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
def isSame(img, template):
    depth, width, height = img.shape[::-1]
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