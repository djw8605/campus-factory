




class ClassAd(dict):
    """
    This class acts as a dictionary object.
    
    """
    def __init__(self, str_classad):
        self.ParseClassad(str_classad)
        
        
    def ParseClassad(self, str_classad):
        ad_dict = {}
        for line in str_classad.split('\n'):
            (key, value) = line.split('=')
            self[key] = value

    def ConvertToOffline(self):
        self["PreviousName"] = self["Name"]
        
    
    def __str__(self):
        str_toreturn = ""
        for key in self.keys():
            str_toreturn += key + " = " + self[key]
        return str_toreturn
    