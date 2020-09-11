import cv2
import glob
import os, sys
import numpy as np

def rename_files(path):
    # path = input('请输入文件路径(结尾加上/)：')
    # 获取该目录下所有文件，存入列表中
    n = 0
    # namelist= []
    fileList = os.listdir(path)
    path_list = fileList.sort()

    for file in fileList:
        # 设置旧文件名（就是路径+文件名）
        oldname = path + file  # os.sep添加系统分隔符
        newname = path + str(n).zfill(8) + '.jpg'
        # namelist.append(newname)
        # print(oldname, '======>', newname)
        os.rename(oldname, newname)
        n+=1
    pass
    print('rename process finished!')

def Image2Video(fps, image_size, image_path, output_path):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    imgs = glob.glob(image_path)
    imgs.sort()

    videoWriter = cv2.VideoWriter(output_path + 'video_snakes.mp4', fourcc, fps, (image_size[1], image_size[0]))  # 最后一个是保存图片的尺寸

    # print(imgs)
    for imgname in imgs:
        frame = cv2.imread(imgname)
        size = np.array(np.shape(frame))
        if not (image_size == size[:2]).all():
            print("image size do not match!")
            sys.exit()
        videoWriter.write(frame)

    print('image to video succeeded!')
    videoWriter.release()


def Video2Image(video_path, output_path):
    vc = cv2.VideoCapture(video_path) #读入视频文件
    try:
        os.makedirs(outpath)
    except:
        print("folder already existed")
    c=0
    rval=vc.isOpened()
    #timeF = 1  #视频帧计数间隔频率
    while rval:   #循环读取视频帧
        c = c + 1
        rval, frame = vc.read()
    #    if(c%timeF == 0): #每隔timeF帧进行存储操作
    #        cv2.imwrite('smallVideo/smallVideo'+str(c) + '.jpg', frame) #存储为图像
        if rval:
            cv2.imwrite(output_path + str(c).zfill(8) + '.jpg', frame) #存储为图像
            cv2.waitKey(1)
        else:
            break
    print('video to images succeeded!')
    vc.release()

if __name__ == '__main__':
    fps = 60  # 保存视频的FPS，可以适当调整
    size = np.array([1080, 1920])
    image_path = "/home/taungdrier/Desktop/video/*.jpg"
    input_path = '/home/taungdrier/Desktop/mapping/map1/'
    # video_path = '/home/taungdrier/Desktop/VID_20200728_174435.mp4'
    video_path = "/home/taungdrier/Pictures/snakes.mp4"
    outpath = '/home/taungdrier/Desktop/'

    # rename_files(input_path)
    Image2Video(fps, size, image_path, outpath)
    # Video2Image(video_path, outpath)