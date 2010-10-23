


import time
import random

class ClassAd(dict):
    """
    This class acts as a dictionary object.
    
    """
    def __init__(self, str_classad):
        self.ParseClassad(str_classad)
        
        
    def ParseClassad(self, str_classad):
        ad_dict = {}
        if len(str_classad) == 0:
            return

        for line in str_classad.split('\n'):
            (key, value) = line.split('=', 1)
            self[key.strip()] = value.strip()

    def ConvertToOffline(self):
        self["PreviousName"] = self["Name"]
        self["Name"] = "offline@%s" % random.randint(1, 10000)
        self["MyCurrentTime"] = self["LastHeardFrom"] = str(int(time.time()))
        
        
    
    def __str__(self):
        str_toreturn = ""
        for key in self.keys():
            str_toreturn += key + " = " + self[key]
        return str_toreturn
    
