import numpy as np
import matplotlib.pyplot as plt

def obmap2coordinaten(obmap):
    ob_coord = np.zeros((1,2))
    shape = np.shape(obmap)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if obmap[i][j] == 1:
                index = np.array([i, j]) * 25 / 150
                ob_coord = np.vstack((ob_coord, index))
    np.delete(ob_coord, 0)
    return ob_coord

def cal_distance(traj):
    size = np.size(traj, axis=0)
    dis_list = []
    for i in range(1, size):
        dis_list.append(np.linalg.norm(traj[i][:]-traj[i-1][:]))
        print('d{order} = {num:.2f}m'.format(order=i, num=dis_list[i-1]))
    dis_sum = sum(dis_list)
    print('total distance = {:.2f}m'.format(dis_sum))

num = 3
traj_list =[]
traj1 = np.array([[-188.96,254.29,7.1356],
                     [-324.7,243.92,5.266],
                     [-394.81,358.42,7.9197],
                     [-138.91,378.82,10.452],
                     [-131.07,255.52,7.511],
                     [-248.76,254.76,6.7823]])

traj2 = np.array([[220.05,163.02,7.7699],
                 [241.06,143.67,6.5175],
                 [158.49,55.142,7.7972],
                 [114.03,96.815,10.023],
                 [-73.892,-63.554,9.3387],
                 [-131.57,2.025,8.943],
                 [214.09,311.72,7.3],
                 [292.61,223.12,7.656],
                 [190.16,137.88,8.384],
                 [212.54,107.67,6.29]])

traj3 = np.array([[-472.16,159.19,10.884],
                  [-239.37,-81.327,7.5974],
                  [-249.92,-90.656,7.896],
                  [-473.34,144.52,11.394]])

traj_list.append(traj1)
traj_list.append(traj2)
traj_list.append(traj3)


if num:
    cal_distance(traj_list[num-1])








# d2 = distance(b, c)
# print(d1)

# print(d2)
# print('total distance is:{:.2f} m'.format(d1 + d2))
# import cv2
# import numpy as np
#
# cap = cv2.VideoCapture(0)
#
# while True:
#     _, frame = cap.read()
#     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     sift = cv2.xfeatures2d.SIFT_create()
#     kp = sift.detect(gray,None)#找到关键点
#
#     img=cv2.drawKeypoints(gray,kp,frame)#绘制关键点
#
#     cv2.imshow('sp',img)
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break
#
# cv2.destroyAllWindows()