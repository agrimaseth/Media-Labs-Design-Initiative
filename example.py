import cv2
import numpy as np
from time import sleep
cap = cv2.VideoCapture('testing.mp4')
sleep(2)
ctr=0
ctr1=0
while( cap.isOpened() ) :
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grey convert
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    #lower_blue = np.array([110,50,50])
    lower_blue = np.array([0,0,128])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if ctr<1:
        for i in range (0,100):
            for j in range(0,100):
                if mask[i][j] == 255 :
                    print hsv[i][j][0],
        ctr=ctr+1
    
    '''for i in range(0,20):
        print "_",
    if ctr1<1:
        for i in range (0,20):
            for j in range(0,20):
                print hsv[i][j],
        ctr1=ctr1+1 '''
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    blur = cv2.GaussianBlur(gray,(5,5),0) 
    ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  
    contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    drawing = np.zeros(img.shape,np.uint8)

    max_area=0
   
    for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)
            if(area>max_area):
                max_area=area
                ci=i
    cnt=contours[ci]
    hull = cv2.convexHull(cnt)
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
                cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                cy = int(moments['m01']/moments['m00']) # cy = M01/M00
              
    centr=(cx,cy)       
    cv2.circle(img,centr,5,[0,0,255],2)       
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
    cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
          
    cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    hull = cv2.convexHull(cnt,returnPoints = False)
    #print cnt
    if(1):
               defects = cv2.convexityDefects(cnt,hull)
               mind=0
               maxd=0
               for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    dist = cv2.pointPolygonTest(cnt,centr,True)
                    #cv2.line(img,start,end,[0,255,0],2)
                    cv2.line(res,far,end,[0,255,0],2)
                    cv2.line(res,start,far,[0,255,0],2)
                    cv2.circle(img,far,5,[0,0,255],-1)
               i=0
    #cv2.imshow('frame',img)
    r=500.0/mask.shape[1]
    dim=(500, int(mask.shape[0]*r))
    mresized=cv2.resize(mask,dim,interpolation=cv2.INTER_AREA)
    cv2.imshow('mask',mresized)
    #cv2.imshow('res',res)
    r2=500.0/drawing.shape[1]
    dim2=(500, int(drawing.shape[0]*r))
    dresized=cv2.resize(drawing,dim2,interpolation=cv2.INTER_AREA)
    cv2.imshow('output',dresized)
    #cv2.imshow('input',img)
                
    k = cv2.waitKey(10)
    if k == 27:
        break