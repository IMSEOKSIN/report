import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

cap = cv2.VideoCapture("video3.mp4")

while(True):
   ret, frame = cap.read()

   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray,(7,7),0)
   edge = cv2.Canny(blur, 150, 150)
   ret, thresh_img = cv2.threshold(edge,91,255,cv2.THRESH_BINARY)
   contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
   
   contours_dict =[]
   
   for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        cv2.rectangle(edge, (x,y), (x+w, y+h), (255, 255, 255), 2)
        contours_dict.append({
          'contour':contour,
          'x':x,
          'y':y,
          'w':w,
          'h':h,
          'cx':x+(w/2),
          'cy':y+(h/2)
        })
        
        MIN_AREA = 50
        MIN_WIDTH,MIN_HEIGHT = 1,4
        MIN_RATIO,MAX_RATIO = 0.25,1.0
        
        possible_contours = []
        
        cnt = 0
        for d in contours_dict:
              area = d['w']*d['h']
              ratio = d['w']/d['h']
              if area > MIN_AREA\
                and d['w']>MIN_WIDTH and d['h']>MIN_HEIGHT\
                and MIN_RATIO<ratio<MAX_RATIO:
                  d['idx'] = cnt
                  cnt += 1
                  possible_contours.append(d)
        for d in possible_contours:
              cv2.rectangle(edge, pt1=(d['x'], d['y']), pt2=(d['x']+d['w'], d['y']+d['h']), 
                  color=(255, 255, 255), thickness=2)
        
   cv2.imshow('frame',edge)
   if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()