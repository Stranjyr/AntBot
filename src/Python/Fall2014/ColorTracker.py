import numpy as np
import cv2
import time


#This class finds and tracks patches of color
#The find tag method returns a list of all x locations of
#colored patches within upper and lower HSV
#
#The getTurn method returns a value of None, -1, 0, or 1, calculated from the list of 
#color patches returned by findTag
 
class Tracker():
    #colors are the high and low values for the HSV
    def __init__(self, lower, upper, r):
        self.lower = lower
        self.upper = upper
        self.r = r ##how far away the tags can be from the center
        self.cap = cv2.VideoCapture(0)
    def findTag(self):

        # Take each frame
        _, frame = self.cap.read()
       
        #lower_blue = np.array([142, 160,120])
        #upper_blue = np.array([179,240,200])
        upper_blue = self.upper
        lower_blue = self.lower
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        cv2.erode(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        cv2.dilate(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        
        cv2.dilate(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        cv2.erode(mask, mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
        
        _, contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        xVals = []
        for cnt in contours:
            
            M = cv2.moments(cnt)
            marea = int(M['m00'])
            if(marea > 100):
                mx = int(M['m10']/M['m00'])
                xVals.append(mx)
            
        return xVals

        
    def getTurn(self):
        #cap = cv2.VideoCapture(0)
        vals = []
        _, w = self.cap.read()
        _, width = w.shape[0:2]
        for i in range(0, 10):
            temp = self.findTag(cap)
            for x in range(len(temp)):
                if len(vals) <= x:
                    vals.append([temp[x], 1])
                else:
                    vals[x][0]+=temp[x]
                    vals[x][1] +=1
        if(vals == []):
            return None
        tags = [] #I stores the locations from the center of the screen for each tag
        for tag in vals: 
            if tag[1]>=2:
                tags.append(tag[0]/tag[1]-width/2.0)
        
        next = min(tags)
        print(next)
        abs = (next**2)**.5
        if(abs<=self.r):
            return 0
        return next/abs
 
 
def main():
    T = Tracker(np.array([132, 150,110]), np.array([179,250,210]), 50)
    
    x = T.getTurn()
    print(x)
    
#main()