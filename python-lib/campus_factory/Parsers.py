import logging
import xml.sax.handler
import os

def RunExternal(command):
    """Run an external command 
    
    @param command: String of the command to execute
    @return: (str(stdout), str(stderr)) of command
    Returns the stdout and stderr
    
    """

    logging.debug("Running external command: %s" % command)
    (stdin, stdout, stderr) = os.popen3(command, 'r')
    str_stdout = stdout.read()
    str_stderr = stderr.read()
    return str_stdout, str_stderr


class AvailableGlideins(xml.sax.handler.ContentHandler):
    
    # Command to query the collector for available glideins
    command = "condor_status -avail -format '<glidein name=\"%s\"/>' 'Name'"
    
    def __init__(self):
        pass

    def GetIdle(self):
        self.idle = 0
        self.found = False

        # Get the xml from the collector
        to_parse, stderr = RunExternal(self.command)
        formatted_to_parse = "<doc>%s</doc>" % to_parse

        # Parse the data
        try:
            xml.sax.parseString(formatted_to_parse, self)
        except xml.sax._exceptions.SAXParseException, inst:
            logging.error("Error parsing:")
            logging.error("command = %s" % self.command)
            logging.error("stderr = %s" % stderr)
            logging.error("stdout = %s" % to_parse)
            logging.error("Error: %s - %s" % ( str(inst), inst.args ))
    
        if not self.found and (len(stderr) != 0):
            logging.error("No valid output received from command: %s"% self.command)
            logging.error("stderr = %s" % stderr)
            logging.error("stdout = %s" % to_parse)
            return None

        return self.idle
    
    def Run(self):
        """
        Generic function for when this class is inherited
        """
        return self.GetIdle()

    def startElement(self, name, attributes):
        if name == "glidein":
            self.idle += 1
            self.found = True


class IdleGlideins(AvailableGlideins):
    
    command = "condor_q -const '(GlideinJob == true) && (JobStatus == 1)' -format '<glidein owner=\"%s\"/>' 'Owner'"
    

class IdleJobs(AvailableGlideins):
    
    command = "condor_q -name %s -const '(GlideinJob =!= true) &&  (JobStatus == 1)' -format '<glidein owner=\"%%s\"/>' 'Owner'"

    def __init__(self, schedd):
        self.command = self.command % schedd


class FactoryID(AvailableGlideins):
    command = "condor_q -const '(IsUndefined(IsFactory) == FALSE)' -format '<factory id=\"%s\"/>' 'ClusterId'"
    
    def startElement(self, name, attributes):
        if name == "factory":
            self.factory_id = attributes.getValue("id")
            self.found = True

    def GetId(self):
        self.GetIdle()
        return self.factory_id

class RunningGlideinsJobs(AvailableGlideins):
    """
    Gets the number of running glidein jobs (condor_q)
    """
    
    command = "condor_q -const '(GlideinJob == true) && (JobStatus == 2)' -format '<glidein owner=\"%s\"/>' 'Owner'"
    

class RunningGlideins(AvailableGlideins):
    """
    Returns the number of startd's reporting to the collector (condor_status)
    """
    
    command = "condor_status -const '(IsUndefined(IS_GLIDEIN) == FALSE) && (IS_GLIDEIN == TRUE)' -format '<glidein name=\"%s\"/>' 'Name'"
    
    
    
    
