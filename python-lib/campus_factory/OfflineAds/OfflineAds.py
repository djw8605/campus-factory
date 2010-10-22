
# I'm lazy
MINUTE = 60
HOUR = MINUTE * 60

from campus_factory.Parsers import RunExternal
import time

class OfflineAds():
    
    def __init__(self, siteunique="GLIDEIN_Site", timekeep=HOUR*24, numclassads=10, lastmatchtime=MINUTE*5):
        """
        Initialize function
        
        @param siteunique: Classad attributed that uniquely identifies a site
        @param timekeep: Seconds to keep the classad
        @param numclassads: Maximum number of classads to keep for each Site
        @param lastmatchtime: Only consider matches that occured between now and now-lastmachtime
        
        """
        self.siteunique = siteunique
        self.timekeep = timekeep
        self.numclassads = numclassads
        self.lastmatchtime = lastmatchtime
        

    def _Initialize(self):
        pass
    
    
    def Update(self):
        
        # Check last match times for an recent match
        matched_sites = self.GetLastMatchedSites()
        
        # Check for expired classads, delete them (OFFLINE_EXPIRE_ADS_AFTER should do this)
        #self.RemoveExpiredClassads()
        
        # Check for new startd's reporting, save them while deleting the older ones (max numclassads)
        
        
        return matched_sites
    
    
    def GetLastMatchedSites(self):
        """
        Return the last matched sites as configured with lastmatchtime
        
        @return: list of sites with last match
        """
        cmd = "condor_status -const '(IsUndefined(Offline) == FALSE) && (Offline == TRUE) && \
                 (IsUndefined(MachineLastMatchTime) == False) && (MachineLastMatchTime > %(matchtime)i) \
                 -format '%%s' '%(siteunique)s' | sort | uniq -c"
        
        query_opts = {"matchtime": int(time.time()) - self.lastmatchtime, "siteunique": self.siteunique}
        new_cmd = cmd % query_opts
        (stdout, stderr) = RunExternal(new_cmd)

        return stdout.split('\n')
        
    
    def RemoveExpiredClassads(self):
        """
        THIS NEEDS TO BE IMPLEMENTED ?
        
        Use condor_advertise to de-advertise expired offline ads.
        It is possible to do this inside condor with OFFLINE_EXPIRE_ADS_AFTER (probably should be done in condor)
        
        
        """
    
    
    def GetUniqueAliveSites(self):
        """
        Get the unique sites that we see right now
        
        @return: list of sites
        
        """
        
        # Is there a better way? Absolutely...
        cmd = "condor_status -format '%%s' '%s' -const '(IsUndefined(Offline) == TRUE)' | sort | uniq"
        (stdout, stderr) = RunExternal(cmd)
        
        return stdout.split('\n')

