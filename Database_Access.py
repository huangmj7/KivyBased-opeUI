#log 

import os 
import datetime

#csv
import csv

#objects
from PLC_CONTROL import PLCControl
from Camera_Access import CameraAccess

class DataProcess:

    def _init_(self,PLC,Camera):

        self.Camera = Camera
        self.PLC = PLC






