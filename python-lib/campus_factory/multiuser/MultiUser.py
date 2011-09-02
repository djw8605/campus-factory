




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
        self.num_idle = 0
        self.num_running = 0
        
    def StartIteration(self):
        """
        Start the interation, resetting the values to 0
        """
        self.num_idle = 0
        self.num_running = 0
        
    def SetIdleRunning(self, idle, running):
        """
        Set the number of idle and running jobs for this user
        
        @param idle: Number of idle jobs for this user
        @param running: Number of running jobs for this user
        """
        self.num_idle = idle
        self.num_running = running

