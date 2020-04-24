import os #log
import random
import time
import datetime

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
        self.updateNo = 0 # # of SetControl being called
        self.logfile = ""
    
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
            if(self.ReturnList[5] < self.SetList[5]):self.ReturnList[5] += random.uniform(1,10) #Randomly generate increase value
            if(self.ReturnList[5] > self.SetList[5]):self.ReturnList[5] -= random.uniform(1,10) #Randomly generate decrease value

            #Feed Rate 
            #Currently Unchange
            self.ReturnList[6] = self.SetList[6]

        return self.ReturnList

    def SetControl(self,t1,t2,t3,t4,s1,f1):

            
            #Update No
            self.updateNo += 1

            #Four Temperature Zone
            self.SetList[0] = t1
            self.SetList[1] = t2
            self.SetList[2] = t3
            self.SetList[3] = t4

            #Speed
            self.SetList[5] = s1

            #Speed
            self.SetList[6] = f1 #Randomly generate

            #Write the setting to log
            f = open(self.logfile,"a")
            t = datetime.datetime.now()
            f.write("Time {}: No.{} Upadte settings\n".format(t,self.updateNo))
            f.write("Set Temperature Zone 1 to {}".format(self.SetList[0]))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 2 to {}".format(self.SetList[1]))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 3 to {}".format(self.SetList[2]))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 4 to {}".format(self.SetList[3]))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Screw Speed {} RPM\n".format(self.SetList[5]))
            f.write("Set Feed Rate to {} mmpr\n".format(self.SetList[6]))

            f.close()

    def SetUser(self,name,access,polymer):

        logintime = datetime.datetime.now().strftime("%Y-%m-%d@%H:%M")
        self.logfile = "myData/log/log-{}.txt".format(logintime)

        f = open(self.logfile,"w") #should the first to write
        t = datetime.datetime.now()
        f.write("Time {}: User {} login with code {}\n".format(t,name,access))
        f.write("Target Polymer: {}\n".format(polymer))
        f.close()


if "__name__" == "__main__":
    
    X = PLCControl()
    X.SetControl(1,2,3,4,5,6)
    
    for i in range(60):
        
        print("Current Second: {}".format(i))
        RL = X.GetSensorReadings()
        print(RL)
        time.sleep(1)
    

