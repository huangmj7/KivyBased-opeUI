import os 
import random
import time
import picamera

import cv2
import imutils
from imutils import perspective
from imutils import contours
import numpy as np
from scipy.spatial.distance import euclidean


class CameraAccess:

    def __init__(self):

        self.Pdiameter = "0"
        self.Start = 0

        self.Image = "" #Current images
        self.ImageNo = 1 #Helper
        self.MaxImage = 12 #Sample ranges
        self.Action = "" #status point
        self.Camera = picamera.PiCamera() #open

    def __del__(self):

        self.Camera.close()

    def TakePicture(self):

        if(self.Action == "ERROR"):return; #Camera failed to open
        my_path = "myData/image" #Given path

        try:
            self.Camera.resolution = (1280,720) #Based on Tom
            #camera.start_preview()
            time.sleep(2) #Warm-up time
            No = "pi{}.jpg".format(self.ImageNo)
            Name = os.path.join(my_path,No)
            self.Camera.capture(Name) #Store in given folder
            self.Image = Name #pdate current images
            self.ImageNo += 1
            if(self.ImageNo == self.MaxImage):self.ImageNo = 0 #only store image within 1 minutes
        except:
            #Camera issues
            self.Action = "ERROR"

     
    def GetDiameter(self):

        image_path = self.Image
        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        edged = cv2.Canny(blur, 50, 100) 
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        #show_images([blur, edged])

        # Find contours
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Sort contours from left to right as leftmost contour is reference object
        if(len(cnts) < 2): return str(-1) #No edge detected
        (cnts, _) = contours.sort_contours(cnts)

        # Remove contours which are not large enough
        cnts = [x for x in cnts if cv2.contourArea(x) > 100]

        #cv2.drawContours(image, cnts, -1, (0,255,0), 3)
        #show_images([image, edged])
        if(len(cnts) < 1): return str(-1) #failed to found fit object

        # Reference object dimensions
        # Here for reference I have used a quarter (24.26 mm in diameter)
        ref_object = cnts[0]
        box = cv2.minAreaRect(ref_object)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dist_in_pixel = euclidean(tl, tr)
        dist_in_mm = 24.26
        pixel_per_mm = dist_in_pixel/dist_in_mm

        # Draw remaining contours
        for cnt in cnts:
            box = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            (tl, tr, br, bl) = box
            cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
            mid_pt_horizontal = (tl[0] + int(abs(tr[0] - tl[0])/2), tl[1] + int(abs(tr[1] - tl[1])/2))
            mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0])/2), tr[1] + int(abs(tr[1] - br[1])/2))
            wid = euclidean(tl, tr)/pixel_per_mm
            ht = euclidean(tr, br)/pixel_per_mm
            cv2.putText(image, "{:.1f}mm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.putText(image, "{:.1f}mm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

           
        cv2.imwrite(self.Image,image)   
        return str(wid) 


            


    def Get(self):

        tp = time.time() - self.Start
        
        #Camera need 2 second to warm : for now
        if(tp > 3 and self.Action != "ERROR"):
            
            self.Start = time.time() #Update at least every five seconds
            self.TakePicture() #Image taking
            self.Pdiameter = self.GetDiameter()#random.random()*100+random.uniform(25,28)
            if(self.Action != "ERROR"):self.Action = "reload"
        elif(self.Action != "ERROR:"):
            self.Action = "wait" #allow error adjustment
            
            
            

        result = []
        result.append(self.Action) #Reloaf image or not
        result.append(self.Pdiameter) #Polymer diameter
        result.append(self.Image) #Image
        return result

