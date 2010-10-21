
import re
import logging

from campus_factory.Parsers import AvailableGlideins
from campus_factory.Parsers import IdleGlideins
from campus_factory.Parsers import IdleJobs
from campus_factory.Parsers import FactoryID
from campus_factory.Parsers import RunningGlideinsJobs
from campus_factory.Parsers import RunningGlideins
from campus_factory.Parsers import RunExternal


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
 
        return cls.instance


class CondorConfig:
    """
    Singleton of the condor config (as reported by condor_config_val -dump)
    """
    __metaclass__ = Singleton
    
    def __init__(self):
        (stdout, stderr) = RunExternal("condor_config_val -dump")
        if len(stdout) == 0:
            error_msg = "Unable to get any output from condor_config_val.  Is condor binaries in the path?"
            raise EnvironmentError(error_msg)
        
        # Parse the stdout
        line_re = re.compile("([\w|\d]+)\s+=\s+(.*)\Z")
        config_dict = {}
        for line in stdout.split('\n'):
            match = line_re.search(line)
            if match == None:
                continue
            (key, value) = match.groups()
            config_dict[key] = value
        
        logging.info("Got %s values from condor_config_val" % len(config_dict.keys()))
        self.config_dict = config_dict
        
    def get(self, key):
        """
        @param key: string key
        @return: string - value corresponding to key or "" if key is non-valid
                        
        """
        if self.config_dict.has_key(key):
            return self.config_dict[key]
        else:
            return ""


class ClusterStatus:
    """
    Gather statistics on the cluster status
    
    
    """

    def __init__(self):
        pass

    def RunExternal(self, command):
        """ 
        Run an external command 
        
        @param command: Shell command to execute
        @return: str - stdout from command
        """
        (stdin, stdout, stderr) = os.popen3(command, 'r')
        str_stdout = stdout.read()
        return str_stdout

    def GetIdleGlideins(self):
        """ 
        Returns the number of glideins idle in the cluster (condor_status -avail) 
        
        @return: int - Number of idle glidein slots.
        """
        availglideins = AvailableGlideins()
        return availglideins.GetIdle()


    def GetIdleGlideinJobs(self):
        """ 
        Returns the number of glidein jobs that are idle (condor_q) 
        
        @return: int - Number of glidein jobs submitted but still idle.
        """
        idleglideins = IdleGlideins()
        return idleglideins.GetIdle()

    def GetIdleJobs(self, schedds):
        """ 
        Returns the number of idle user jobs (condor_q) 
        
        @param schedds: List [] of schedd names to check for idle jobs.
        @return: int - Number of jobs idle
        """
        sumidlejobs = 0
        for schedd in schedds:
            idlejobs = IdleJobs(schedd)
            schedd_idlejobs = idlejobs.GetIdle()
            if schedd_idlejobs != None:
                sumidlejobs += schedd_idlejobs

        return sumidlejobs


    def GetFactoryID(self):
        """
        Returns the condor ClusterId for the factory.
        
        @return: str - ClusterId of the factory
        """
        factoryID = FactoryID()
        return factoryID.GetId()
    
    def GetRunningGlideinJobs(self):
        """
        @return: int - Number of running glidein jobs
        """
        running = RunningGlideinsJobs()
        return running.Run()
        
    def GetRunningGlideins(self):
        """
        @return: int - Number of running glidein startds
        """
        running = RunningGlideins()
        return running.Run()
    
    
    
