import os
import time
from datetime import datetime
import csv

class DataManager:

	def __init__(self):
            
            self.logAddress = ""
            self.cvsAddress = ""
            self.logCreated = False
            
            logintime = datetime.now().strftime("%Y-%m-%d@%H:%M")
            self.logAddress = "myData/log/log-{}.txt".format(logintime)
            self.cvsAddress = "myData/log/log-{}.csv".format(logintime)



	def CreateCSV(self,name,access,polymer):
            
            fields = ["Temperature 1","Temperature 2","Temperature 3","Temperature 4","Pressure","Speed","Feed Rate","Time interval","Polymer diameter","Image address"] 
            
            with open(self.cvsAddress, "w") as csvfile:
                
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(fields) 


	def WriteCSV(self,fields):
            
            with open(self.cvsAddress, "a") as csvfile:
                
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(fields)


	def CreateLog(self,name,access,polymer):
            
            self.CreateCSV(name,access,polymer)
            
            f = open(self.logAddress,"w") #should the first to write
            t = datetime.now()
            f.write("Time {}: User {} login with code {}\n".format(t,name,access))
            f.write("Target Polymer: {}\n".format(polymer))
            self.logCreated = True
            f.close()

	def WriteLog(self,updateNo,t1,t2,t3,t4,s1,f1):
            
            if(not self.logCreated): return
            f = open(self.logAddress,"a")
            t = datetime.now()
            f.write("Time {}: No.{} Upadte setting\n".format(t,updateNo))
            f.write("Set Temperature Zone 1 to {}".format(t1))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 2 to {}".format(t2))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 3 to {}".format(t3))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Temperature Zone 4 to {}".format(t4))
            f.write(u'\N{DEGREE SIGN}'+"C\n")
            f.write("Set Screw Speed {} RPM\n".format(s1))
            f.write("Set Feed Rate to {} mmpr\n".format(f1))
            
            f.close()


