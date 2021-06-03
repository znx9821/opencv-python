# -*- coding: utf-8 -*-
"""
Created on Fri May 21 12:46:26 2021
@author: znx

1. scan and list all accessable cameras
2. start record and save images in folders
3. close windows to quit record
"""

import cv2
import datetime
import time
#from multiprocessing import Process

def list_ports(): #Test the ports and returns a tuple with the available ports and the ones that are working.
    is_working = True
    dev_port = 0
    available_ports = []
    working_ports = []
    selected_ports =[]
    
    while is_working:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            is_working = False
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            if is_reading: 
                print("Port %s is working" %dev_port) 
                working_ports.append(dev_port)
                text = "selected: press [s]; Next: press any other key"
                org = (40, 80)
                fontFace = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 0.5
                fontcolor = (0, 255, 0) # BGR
                # 图片 添加的文字 文字位置 字体 字体大小 字体颜色 
                cv2.putText(img, text, org, fontFace, fontScale, fontcolor)
                cv2.imshow("port"+str(dev_port),img)
                k = cv2.waitKey(0) & 0xFF
                if k == ord('s'):
                    selected_ports.append(dev_port)
                    print("camera %s is selected" %dev_port)
                cv2.destroyAllWindows()
            else:
                print("Port %s is present but does not reads" %dev_port) #print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        camera.release()
        dev_port +=1
    #camera.release()    
    #cv2.destroyAllWindows()
    return available_ports,working_ports,selected_ports #所有可以获得的port在available_ports,  其中可以读取的在working_ports

def getVideoProperty(singleAvi):
    cap = cv2.VideoCapture(singleAvi)
    fps = cap.get(cv2.CAP_PROP_FPS)  # 获取视频fps
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # 获取视频宽度
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # 获取视频高度
    cap.release()
    videoProp={'fps':fps, 'wid':int(width), 'hei':int(height)}
    return videoProp

def writeJpg(webcamList,targetPath):
    #vidP = getVideoProperty(singleAvi)
    #fps = vidP['fps']  #这里是表示每秒有多少帧，同时也表示多少帧输出1帧。如果需要2秒输出一张图片，就把这里改为 fps = 2 * vidP['fps']
    #对于webcam来说，python获取的fps是不准确的，修改为定时拍照和save
    webcamNumber=len(webcamList)
    if len(webcamList)<1:
       print("no webcam selected")
       return
    else:
       capList=list()
       retList=list()
       frameList=list()
       for i in webcamList:
           capList.append(cv2.VideoCapture(i))
           if not (capList[-1].isOpened()):
               print("Could not open video device:"+str(i)) 
               return
           ret,frame = capList[-1].read()    # ret表示是否成功获取帧
           retList.append(ret)
           frameList.append(frame)
                
    for i in range(0,webcamNumber): #判断所有的camera均正确读取到帧才继续
        ret = ret and retList[i]
        cv2.namedWindow("preview-"+str(webcamList[i]),cv2.WINDOW_FREERATIO)
        # cv2.namedWindow('result', cv2.WINDOW_NORMAL)   # 窗口大小可以改变
        # cv2.namedWindow('result', cv2.WINDOW_FREERATIO)   # 窗口大小自适应比例
        # cv2.namedWindow('result', cv2.WINDOW_KEEPRATIO)   # 窗口大小保持比例
        cv2.resizeWindow("preview-"+str(webcamList[i]),480,320) #设置预览窗口的大小
    
    count = 0
    org = (40, 80) #添加的文字位置
    fontFace = cv2.FONT_HERSHEY_COMPLEX #添加的文字字体
    fontScale = 0.5 #添加的字体大小
    fontcolor = (0, 255, 0) # #添加的字体颜色
    print("the number of selected cameras: ",webcamNumber)
    while(ret):
        time_text = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
        for i in range(0,webcamNumber):
            cv2.putText(frameList[i], time_text, org, fontFace, fontScale, fontcolor) # 图片 添加的文字 文字位置 字体 字体大小 字体颜色
            cv2.imwrite(targetPath+str(webcamList[i])+'-'+str(count)+'.jpg',frameList[i])
            print('write img:'+targetPath+str(webcamList[i])+'-'+str(count)+'.jpg')
            cv2.imshow("preview-"+str(webcamList[i]),frameList[i])
            if cv2.waitKey(1) & 0xFF == ord('q'): #如果按下q，就结束采集
                break
        ret = True #初始化为True
        time.sleep(1) #采样频率，此处设置暂停 1秒
        for i in range(0,webcamNumber):
            retList[i],frameList[i] = capList[i].read()
            ret = ret and retList[i]
        count += 1 
    for i in range(0,webcamNumber):
        capList[i].release()     
    cv2.destroyAllWindows()
    print("stop recording on "+str(count)+' time: '+time_text)
    return    

#首先需要运行 a,b,c=list_ports()以获得所有可以使用的camera的列表
a,b,c=list_ports()  # a,b,c分别表示可获得的port,可读取的port和被选中的port
tempPath=input("please input the directory you want to save .jpg here, end with '/' :")
writeJpg(c,tempPath)

"""
video = cv2.VideoCapture(1)
num_frames = 120
start = time.time()
for i in range(0, num_frames):
    ret, frame = video.read()
end = time.time()
seconds = end - start
fps  = num_frames / seconds  
video.release()
"""

#for singleAvi in c:
#    p=Process(target=writeJpg(singleAvi,tempPath))
#p.start()
   # writeJpg(singleAvi,tempPath)
#writeJpg(0,tempPath)
