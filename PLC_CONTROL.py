import os #log
import random
import time

#QiXin
#12 readings per second
#Temperature range 250-280
#Pressure range 100-1000
#random.uniform(Min,Max)

class PLCControl:

    def __init__(self):
         
        #Adapt to dict() Later
        self.ReturnList = [0,0,0,0,0,0,0] #return sensors reading in a list form [T1,T2,T3,T4,P1,S1,F1]
        self.SetList = [0,0,0,0,0,0,0] #Same format as above
        self.Start = time.time() #Start reading
    
    def GetSensorReadings(self):

        tp = time.time() - self.Start
        if((time.time() - self.Start) >= 5):
            
            self.Start = time.time() #Update at least every five seconds
            
            #Four Temperature Zone
            self.ReturnList[0] = random.uniform(250,280)
            self.ReturnList[1] = random.uniform(250,280)
            self.ReturnList[2] = random.uniform(250,280)
            self.ReturnList[3] = random.uniform(250,280)

            #Pressure
            self.ReturnList[4] = random.uniform(100,1000)

            #Speed
            if(self.ReturnList[5] < self.SetList[5]):self.ReturnList[5] += random.uniform(1,5) #Randomly generate increase value
            if(self.ReturnList[5] > self.SetList[5]):self.ReturnList[5] -= random.uniform(1,5) #Randomly generate decrease value

            #Feed Rate 
            #Currently Unchange
            self.ReturnList[6] = self.SetList[6]

        return self.ReturnList

    def SetControl(self,t1,t2,t3,t4,s1,f1):

            #Four Temperature Zone
            self.SetList[0] = t1
            self.SetList[1] = t2
            self.SetList[2] = t3
            self.SetList[3] = t4

            #Speed
            self.SetList[5] = s1

            #Speed
            self.SetList[6] = f1 #Randomly generate

if "__name__" == "__main__":
    
    X = PLCControl()
    X.SetControl(1,2,3,4,5,6)
    
    for i in range(60):
        
        print("Current Second: {}".format(i))
        RL = X.GetSensorReadings()
        print(RL)
        time.sleep(1)
    

