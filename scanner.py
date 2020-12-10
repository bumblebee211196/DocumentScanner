"""
scanner.py: A simple document scanner that accepts the Image PATH as an argument.
"""

__author__ = "S Sathish Babu"
__date__ = "10/12/20 Thursday 1:11 PM"
__email__ = "sathish.babu@zohocorp.com"

import argparse
import numpy as np
import cv2
import imutils


def order_points(pts):
    """Order the given set of coordinates as top-left, top-right, bottom-right and bottom-left"""
    rect = np.zeros((4, 2), dtype='float32')
    _sum = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(_sum)]
    rect[2] = pts[np.argmax(_sum)]
    _diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(_diff)]
    rect[3] = pts[np.argmax(_diff)]
    return rect


ap = argparse.ArgumentParser(prog='Document Scanner')
ap.add_argument('-i', '--image', required=True, help='Path to Image file', type=str)
args = vars(ap.parse_args())

# Step 1: Find edges
image_path = args['image']
print(image_path)
image = cv2.imread(image_path)
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
blurred = cv2.GaussianBlur(gray, (5, 5), 0)     # Image smoothening for noise removal
edged = cv2.Canny(blurred, 100, 250)            # Edge detection

cv2.imshow("Image", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Blurred", blurred)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 2: Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        target = approx
        break

cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 3: Bird's eye view
rect = order_points(target.reshape(4, 2) * ratio)
tl, tr, br, bl = rect

width_a = np.sqrt(((tl[0] - tr[0]) ** 2) + ((tl[1] - tr[1]) ** 2))
width_b = np.sqrt(((bl[0] - br[0]) ** 2) + ((bl[1] - br[1]) ** 2))
width = max(int(width_a), int(width_b))

height_a = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
height_b = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
height = max(int(height_a), int(height_b))

dest = np.array([
    [0, 0],
    [width-1, 0],
    [width-1, height-1],
    [0, height-1]
], dtype='float32')
mat = cv2.getPerspectiveTransform(rect, dest)
warped = cv2.warpPerspective(orig, mat, (width, height))

cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
cv2.destroyAllWindows()
