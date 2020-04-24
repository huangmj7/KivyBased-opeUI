import os #log
import random
import time

class CameraAccess:

    def __init__(self):

        self.Pdiameter = 0
        self.Start = 0

        self.Image = "" #Local file images
        self.ImageNo = 0 #Helper

    def Get(self):

        tp = time.time() - self.Start
        if(tp):
            
            self.Start = time.time() #Update at least every five seconds
            self.Pdiameter = random.random()*100+random.uniform(25,28)
            image_path = "myData/image"
            self.image = os.path.join(image_path,"pi{}.JPG".format(self.ImageNo)) #same folder
            #only 3 photo now
            if(self.ImageNo < 2):
                self.ImageNo += 1
            else:
                self.ImageNo = 0

        result = []
        tp = int(time.time() - self.Start)
        result.append(str(tp)) #Get time
        result.append(str(int(self.Pdiameter))) #Polymer diameter
        result.append(self.image) #Image
        return result
