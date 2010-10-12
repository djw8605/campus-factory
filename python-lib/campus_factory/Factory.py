
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

        # Read in the configuration file
        self.config_file = options.config
        self.config = ConfigParser.ConfigParser()
        files_read = self.config.read([self.config_file])

        # check if no files read in
        if len(files_read) < 1:
            sys.stderr.write("No configuration files found.  Location = %s\n" % self.config_file)
            sys.exit(1)
            
        self._SetLogging()
        try:
            self.condor_config = CondorConfig()
        except Exception:
            logging.error("Unable to get the condor configuration.  If no condor configuration, assuming condor is not available.  Exiting...")
            raise Exception("Unable to get the condor configuration.  If no condor configuration, assuming condor is not available.  Exiting...")

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
        
        



    def Start(self):
        """ 
        Start the Factory 
        
        """


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
            else:
                schedds = self.condor_config.get('FLOCK_FROM').split(",")
                
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
            if max([idlejobs, idleslots]) < idleuserjobs:
                logging.info("Submtting 1 glidein")
                self.SubmitGlideins(1)

            self.SleepFactory()



    def SleepFactory(self):
        sleeptime = int(self.config.get("general", "iterationtime"))
        logging.info("Sleeping for %i seconds" % sleeptime)
        time.sleep(sleeptime)

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
        (stdout, stderr) = RunExternal("condor_submit %s" % file)
        logging.debug("stdout: %s" % stdout)
        logging.debug("stderr: %s" % stderr)



