
import ConfigParser
import sys
import time
import logging
import logging.handlers
import os

from campus_factory.ClusterStatus import ClusterStatus
from campus_factory.ClusterStatus import CondorConfig
from campus_factory.Parsers import RunExternal

class Factory:
    """
    The main class of the factory.  Designed to be run inside the condor scheduler.
    
    @author: Derek Weitzel (dweitzel@cse.unl.edu)
    
    """
    def __init__(self, options):
        """
        Initialization function.
        
        @param options: A set of options in the form of an options parser
                Required options: config - location of configuration File
        """
        
        self.options = options

        
    
    def Intialize(self):
        """
        
        Function to initialize the factory's variables such as configuration
        and logging
        """
        # Read in the configuration file
        self.config_file = self.options.config
        self.config = ConfigParser.ConfigParser()
        files_read = self.config.read([self.config_file])

        # check if no files read in
        if len(files_read) < 1:
            sys.stderr.write("No configuration files found.  Location = %s\n" % self.config_file)
            sys.exit(1)
            
        self._SetLogging()
        try:
            self.condor_config = CondorConfig()
        except EnvironmentError, inst:
            logging.exception(str(inst))
            raise inst
        
        
    def _SetLogging(self):
        """
        Setting the logging level and set the logging.
        """
        logging_levels = {'debug': logging.DEBUG,
                          'info': logging.INFO,
                          'warning': logging.WARNING,
                          'error': logging.ERROR,
                          'critical': logging.CRITICAL}

        level = logging_levels.get(self.config.get("general", "loglevel"))
        logdirectory = self.config.get("general", "logdirectory")
        handler = logging.handlers.RotatingFileHandler(os.path.join(logdirectory, "campus_factory.log"),
                        maxBytes=10000000, backupCount=5)
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
        
        
    def Restart(self):
        status = ClusterStatus()
        
        # Get the factory id
        factoryID = status.GetFactoryID()
        
        # Hold then release the factory in the queue
        (stderr, stdout) = RunExternal("condor_hold %s" % factoryID)
        print "Stderr = %s" % stderr.strip()
        #print "Stdout = %s" % stdout.strip()
        
        (stderr, stdout) = RunExternal("condor_release %s" % factoryID)
        print "Stderr = %s" % stderr.strip()
        #print "Stdout = %s" % stdout.strip()
        
    
    
    def Stop(self):
        status = ClusterStatus()
        
        # Get the factory id
        factoryID = status.GetFactoryID()
        
        # Remove the factory job
        (stderr, stdout) = RunExternal("condor_rm %s" % factoryID)
        print "Stderr = %s" % stderr.strip()



    def Start(self):
        """ 
        Start the Factory 
        
        """
        self.Intialize()

        status = ClusterStatus()

        # First, daemonize?

        while 1:
            logging.info("Starting iteration...")

            # Check for idle glideins (idle startd's)
            idleslots = status.GetIdleGlideins()
            if idleslots == None:
                logging.info("Received None from idle glideins, going to try later")
                self.SleepFactory()
                continue
            logging.debug("Idle glideins = %i" % idleslots)
            if idleslots >= int(self.config.get("general", "MAXIDLEGLIDEINS")):
                logging.info("Too many idle glideins")
                self.SleepFactory()
                continue

            # Check for idle glidein jobs
            idlejobs = status.GetIdleGlideinJobs()
            if idlejobs == None:
                logging.info("Received None from idle glidein jobs, going to try later")
                self.SleepFactory()
                continue
            logging.debug("Queued jobs = %i" % idlejobs)
            if idlejobs >= int(self.config.get("general", "maxqueuedjobs")):
                logging.info("Too many queued jobs")
                self.SleepFactory()
                continue


            # Check for idle jobs to flock from
            if self.config.has_option("general", "FLOCK_FROM"):
                schedds = self.config.get("general", "FLOCK_FROM").split(",")
                logging.debug("Using FLOCK_FROM from the factory config.")
            else:
                schedds = self.condor_config.get('FLOCK_FROM').split(",")
                logging.debug("Using FLOCK_FROM from the condor configuration")
                
            logging.debug("Schedds to query: %s" % str(schedds))
            idleuserjobs = status.GetIdleJobs(schedds)
            if idleuserjobs == None:
                logging.info("Received None from idle user jobs, going to try later")
                self.SleepFactory()
                continue
            logging.debug("Idle jobs = %i" % idleuserjobs)
            if idleuserjobs < 1:
                logging.info("No idle jobs")
                self.SleepFactory()
                continue

            # Got this far, so submit some glideins
            #logging.debug("idleslots = %i, idleuserjobs = %i" % (idleslots, idleuserjobs))
            
            # Determine how many glideins to submit
            num_submit = self.GetNumSubmit(idleslots, idlejobs, idleuserjobs)
            logging.info("Submitting %i glidein jobs", num_submit)
            self.SubmitGlideins(num_submit)

            self.SleepFactory()



    def SleepFactory(self):
        sleeptime = int(self.config.get("general", "iterationtime"))
        logging.info("Sleeping for %i seconds" % sleeptime)
        time.sleep(sleeptime)
        
        
    def GetNumSubmit(self, idleslots, idlejobs, idleuserjobs):
        """
        Calculate the number of glideins to submit.
        
        @param idleslots: Number of idle startd's
        @param idlejobs: Number of glideins in queue, but not active
        @param idleuserjobs: Number of idle user jobs from FLOCK_FROM
        
        @return: int - Number of glideins to submit
        """
        
        # If we have already submitted enough glideins to fufill the request,
        # don't submit more.
        if max([idlejobs, idleslots]) >= idleuserjobs:
            return 0
        
        status = ClusterStatus()
        
        # Check that running glideins are reporting to the collector
        running_glidein_jobs = status.GetRunningGlideinJobs()
        running_glideins = status.GetRunningGlideins()
        if ((running_glidein_jobs * .9) > running_glideins):
            return 0
        
        # Ok, so now submit until we can't submit any more, or there are less user jobs
        return min([self.config.get("general", "maxqueuedjobs") - idlejobs, idleuserjobs])
        
        

    def SubmitGlideins(self, numSubmit):
        """
        Submit numSubmit glideins.
        
        @param numSubmit: The number of glideins to submit.
        """
        # Substitute values in submit file
        file = "share/glidein_jobs/job.submit.template"

        # Submit jobs
        for i in range(numSubmit):
            self.SingleSubmit(file)

        # Delete the submit file

    def SingleSubmit(self, file):
        """
        Submit a single glidein job
        
        @param file: The file (string) to submit
        
        """
        
        # TODO: These options should be moved to a better location
        options = {"WN_TMP": self.config.get("general", "worker_tmp"), \
                   "GLIDEIN_HOST": self.condor_config.get("CONDOR_HOST"), \
                   "GLIDEIN_Site": self.condor_config.get("COLLECTOR_NAME")}
        
        if self.config.has_option("general", "GLIDEIN_Site"):
            options["GLIDEIN_Site"] = self.config.get("general", "GLIDEIN_Site")
        
        options_str = ""
        for key in options.keys():
            options_str += " -a %s=\"%s\"" % (key, options[key])
            
        (stdout, stderr) = RunExternal("condor_submit %s %s" % (file, options_str))
        logging.debug("stdout: %s" % stdout)
        logging.debug("stderr: %s" % stderr)



