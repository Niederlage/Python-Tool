import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

def remove_color(image, color):
    blue_c, green_c, red_c = cv.split(image)
    # cv.imshow('b',blue_c)
    # cv.imshow('r', red_c)
    # cv.imshow('g', green_c)
    # cv.waitKey(5000)
    # 多传入一个参数cv2.THRESH_OTSU，并且把阈值thresh设为0，算法会找到最优阈值
    thresh, ret = cv.threshold(red_c, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # 实测调整为95%效果好一些
    filter_condition = int(thresh * 0.95)
    color_thesh = []
    if 'red' in color:
        _, color_thresh = cv.threshold(red_c, filter_condition, 255, cv.THRESH_BINARY)
    elif 'green' in color:
        _, color_thresh = cv.threshold(green_c, filter_condition, 255, cv.THRESH_BINARY)
    elif 'blue' in color:
        _, color_thresh = cv.threshold(green_c, filter_condition, 255, cv.THRESH_BINARY)
    # 把图片转回 3 通道
    result_img = np.expand_dims(color_thresh, axis=2)
    result_img = np.concatenate((result_img, result_img, result_img), axis=-1)
    return red_c

path = os.getcwd()
file = path + '/1map2.png'
img = cv.imread(file)
print(np.shape(img))
gray = remove_color(img, 'red')
cv.imshow('img',gray)
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite('map2_gray.jpg', gray)

cv.waitKey(1000)
cv.destroyAllWindows()
# print(np.shape(gray))
shape = np.shape(gray)
# ob =[]
# for i in range(shape[0]):
#     for j in range(shape[1]):
#         if gray[i][j] <= 70:
#             index = np.array([i,j])/6
#             ob.append(index)
# print(np.shape(ob))
for i in range(shape[0]):
    for j in range(shape[1]):
        if gray[i][j] > 70:
            gray[i][j] = 0
        else:
            gray[i][j] = 1

np.save("obstacle_loc.npy", gray)

