




class SingleUser:
    """
    This class is to represent a single user in the system.
    
    """
    
    def __init__(self, username):
        """
        Basic init function
        @param username: username to represent
        """
        self.username = username
        self.num_idle_jobs = 0
        self.num_idle_glideins = 0
        self.num_running = 0
        
    def StartIteration(self):
        """
        Start the interation, resetting the values to 0
        """
        self.num_idle = 0
        self.num_running = 0
        
    def SetIdleJobs(self, idle_jobs):
        """
        Set the number of idle and running jobs for this user
        
        @param idle_jobs: Number of idle remote jobs for this user
        """
        self.num_idle_jobs = idle_jobs
    
    def SetIdleGlideins(self, idle_glideins):
        """
         @param idle_glideins: Number of idle glideins on this resource
        """
        self.num_idle_glideins = idle_glideins
        
        
    def SetRunningJobs(self, running_jobs):
        """
        @param running: Number of running jobs for this user
        """
        self.num_running = running_jobs

