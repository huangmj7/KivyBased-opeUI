#Kivy 
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.clock import Clock

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty,NumericProperty, StringProperty,ListProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.window import Window
from kivy_garden.graph import LinePlot ,MeshLinePlot
from kivy.animation import Animation
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
#
import os
from os.path import dirname, join
import time

import random
from threading import Thread
#Simulation class
from PLC_CONTROL import PLCControl
from Camera_Access import CameraAccess
from DataManager import DataManager

#Global
global piCamera 
global PLC #PLCControl Object
global DM

def Simulator():

    #Mimic PLC running
    while True:

        time.sleep(1) #get sample every one second
        #Store 5 minutes == 300 seconds data
        DS = PLC.GetSensorReadings()

        global CameraSet
        #try:
            #CameraSet = piCamera.Get() #Camera
        

        #Temperatur Zone 1
        global Dataset
        if(len(DataSet["T1"]) == 300):
            #Re-new data
            DataSet["T1"] = []
            DataSet["T2"] = []
            DataSet["T3"] = []
            DataSet["T4"] = []
            DataSet["P1"] = []
            DataSet["S1"] = []
            DataSet["F1"] = []


        DataSet["T1"].append(DS[0])
        DataSet["T2"].append(DS[1])
        DataSet["T3"].append(DS[2])
        DataSet["T4"].append(DS[3])
        DataSet["P1"].append(DS[4])
        DataSet["S1"].append(DS[5])
        DataSet["F1"].append(DS[6])




#graph
#using reference https://github.com/atuldo/real-time-plot-microphone-kivy


class Login(Screen):

	location = "login"

	def enter(self):
            
            name = self.ids.name.text
            access = self.ids.access.text
            polymer = self.ids.polymer.text
            print("Name: ", name)
            print("Access: ", access)
            print("Polymer: ", polymer)
            #Allow log in only when all three data are entered
            #Verification conduct here
            if(len(name) > 0 and len(access) > 0 and len(polymer) > 0):
                self.location = "menu"
                DM.CreateLog(name,access,polymer)

class Menu(Screen):
    pass

class SetControl(Screen):

    #class object
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    s1 = 0
    f1  = 0

    def temp1(self):

        text = self.ids.temp1.text
        if(len(text) > 0):self.t1 = int(text)

    def temp2(self):
        
        text = self.ids.temp2.text
        if(len(text) > 0):self.t2 = int(text)

    def temp3(self):
        
        text = self.ids.temp3.text
        if(len(text) > 0):self.t3 = int(text)

    def temp4(self):
        
        text = self.ids.temp4.text
        if(len(text) > 0):self.t4 = int(text)

    def screw(self):
        
        text = self.ids.screw.text
        if(len(text) > 0):self.s1 = int(text)

    def feed(self):
        
        text = self.ids.feed.text
        if(len(text) > 0):self.f1 = int(text)

    def send(self):
        print("Temp Zone 1: ", self.t1)
        print("Temp Zone 2: ", self.t2)
        print("Temp Zone 3: ", self.t3)
        print("Temp Zone 4: ", self.t4)
        print("Temp Screw Speed: ", self.s1)
        print("Temp Feed Rate: ", self.f1)
        PLC.SetControl(self.t1,self.t2,self.t3,self.t4,self.s1,self.f1)
        DM.WriteLog(self,self.t1,self.t2,self.t3,self.t4,self.s1,self.f1)

class ViewCurrentData(Screen):

    T1 = StringProperty()
    T2 = StringProperty()
    T3 = StringProperty()
    T4 = StringProperty()
    P1 = StringProperty()
    S1 = StringProperty()
    F1 = StringProperty()
    PD1 = StringProperty()

    def __init__(self, **kwargs):
        super(ViewCurrentData, self).__init__(**kwargs)
        self.T1 = "-1"
        self.T2 = "-1"
        self.T3 = "-1"
        self.T4 = "-1"
        self.P1 = "-1"
        self.S1 = "-1"
        self.F1 = "-1" #Only change once since sensor not yet being set up
        self.PD1 = "-1"

        self.getCurrent()

    def on_pre_enter(self, **kwargs):
        self.getCurrent()

    def getCurrent(self):
        Clock.schedule_interval(self.get_value, 1) #One second

    def get_value(self,dt):

       DS = PLC.GetSensorReadings()
       

       self.T1 = str(int(DS[0]))
       self.T2 = str(int(DS[1]))
       self.T3 = str(int(DS[2]))
       self.T4 = str(int(DS[3]))
       self.P1 = str(int(DS[4]))
       self.S1 = str(int(DS[5]))
       self.F1 = str(int(DS[6]))
       self.PD1 = str(int(CameraSet[1]))

       temp = []
       temp.extend(DS)
       temp.extend(CameraSet) 
       DM.WriteCSV(temp)


    def stop(self):
        Clock.unschedule(self.get_value)


class ViewPastData(Screen,BoxLayout):
	pass
       




class ViewCamera(Screen):

    pd = StringProperty()
    pic = StringProperty()

    def __init__(self, **kwargs):
        
        super(ViewCamera, self).__init__(**kwargs)
        self.pd = "-1"
        self.pic = 'myData/image/test.jpg' #Default picture
        self.getCurrent()


    def getCurrent(self):
        Clock.schedule_interval(self.get_value, 1)

    def get_value(self,dt):
        
        #print(CameraSet) 
        self.pd = CameraSet[1]
        self.pic = CameraSet[2]
        if(CameraSet[0] == "reload"):self.ids['image'].reload()
        #if(CameraSet[0] == "ERROR") Waring pop up


    def stop(self):
        Clock.unschedule(self.get_value)


#Source: https://github.com/atuldo/real-time-plot-microphone-kivy
class ViewGraph(Screen,BoxLayout):

    #Background and line color
    BC = ListProperty()
    BC = [[1, 0, 0, 1],[1,0.5,0,1],[1,1,0,1],[0,1,0,1],[0,1,1,1],[0,0,1,1],[1,0,1,1]]
 
    def __init__(self,**kwargs):

        super(ViewGraph, self).__init__(**kwargs)
        lw = 1.5
        self.plotT1 = LinePlot(line_width = lw,color=self.BC[0]) #Red
        self.plotT2 = LinePlot(line_width = lw,color=self.BC[1]) #Blue
        self.plotT3 = LinePlot(line_width = lw,color=self.BC[2]) #Yellow
        self.plotT4 = LinePlot(line_width = lw,color=self.BC[3]) #Green
        self.plotP1 = LinePlot(line_width = lw,color=self.BC[4]) #Purple
        self.plotS1 = LinePlot(line_width = lw,color=self.BC[5]) #White
        self.plotF1 = LinePlot(line_width = lw,color=self.BC[6]) #Orange
        self.inGraph = []
        #Be ready to plot
        Clock.schedule_interval(self.get_value, 1)

        #self.Bolds = [True,True,True,True,True,True,True]

    def on_pre_enter(self, **kwargs):
        #Be ready to plot
        Clock.schedule_interval(self.get_value, 1)

    def update(self,Line):

        if(Line in self.inGraph):
            self.ids.graph.remove_plot(Line)
            self.inGraph.remove(Line)
            
        else:
            self.ids.graph.add_plot(Line)
            self.inGraph.append(Line)

    def stop(self):
         Clock.unschedule(self.get_value)

    def get_value(self, dt):
        self.plotT1.points = [(i, j) for i, j in enumerate(DataSet["T1"])]
        self.plotT2.points = [(i, j) for i, j in enumerate(DataSet["T2"])] 
        self.plotT3.points = [(i, j) for i, j in enumerate(DataSet["T3"])]
        self.plotT4.points = [(i, j) for i, j in enumerate(DataSet["T4"])]
        self.plotP1.points = [(i, j) for i, j in enumerate(DataSet["P1"])]
        self.plotS1.points = [(i, j) for i, j in enumerate(DataSet["S1"])]
        self.plotF1.points = [(i, j) for i, j in enumerate(DataSet["F1"])]



    def T1(self):
        self.update(self.plotT1)
        
    def T2(self):
        self.update(self.plotT2)

   
    def T3(self):
        self.update(self.plotT3)
    
    def T4(self):
        self.update(self.plotT4)

    def P1(self):
        self.update(self.plotP1)

    def S1(self):
        self.update(self.plotS1)
     
    def F1(self):
        self.update(self.plotF1)



class ScreenApp(App):

    def build(self):
        
        Builder.load_file("opeUI.kv") #Loading kv file
        Manager = ScreenManager()
        Manager.add_widget(Login(name = 'login'))
        Manager.add_widget(Menu(name = 'menu'))
        Manager.add_widget(SetControl(name = 'setcontrol'))
        Manager.add_widget(ViewCurrentData(name = 'currentdata'))
        Manager.add_widget(ViewPastData(name = 'pastdata'))
        Manager.add_widget(ViewGraph(name = 'graph'))
        Manager.add_widget(ViewCamera(name = 'camera'))
        
        return Manager

    def on_request_close(self,*args):

        print("App is closing.......")
        return True

#Global
 
piCamera= CameraAccess()
CameraSet = ["wait","0","myData/image/test.jpg" ]

PLC = PLCControl() 
DataSet = dict()
DM = DataManager()

DataSet["T1"] = []
DataSet["T2"] = []
DataSet["T3"] = []
DataSet["T4"] = []
DataSet["P1"] = []
DataSet["S1"] = []
DataSet["F1"] = []


#Thread
get_level_thread = Thread(target = Simulator)
get_level_thread.daemon = True
get_level_thread.start()
ScreenApp().run()
