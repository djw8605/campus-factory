import logging
import xml.sax.handler
import os
from popen2 import Popen3
from select import select

def RunExternal(command, str_stdin=""):
    """Run an external command 
    
    @param command: String of the command to execute
    @param stdin: String to put put in stdin
    @return: (str(stdout), str(stderr)) of command
    Returns the stdout and stderr
    
    """

    logging.info("Running external command: %s" % command)
    popen_inst = Popen3(command, True)
    logging.debug("stdin = %s" % str_stdin)
    str_stdout = str_stderr = ""
    while 1:
        read_from_child = -1
        if not popen_inst.tochild.closed:
            (rlist, wlist, xlist) = select([popen_inst.fromchild, popen_inst.childerr], \
                                           [popen_inst.tochild], [])
        else:
            (rlist, wlist, xlist) = select([popen_inst.fromchild, popen_inst.childerr], [], [])

        if popen_inst.fromchild in rlist:
            tmpread =  popen_inst.fromchild.read(4096)
            read_from_child = len(tmpread)
            str_stdout += tmpread
        
        if popen_inst.childerr in rlist:
            tmpread = popen_inst.childerr.read(4096)
            read_from_child += len(tmpread)
            str_stderr += tmpread
            
        if popen_inst.tochild in wlist and len(str_stdin) > 0:
            popen_inst.tochild.write(str_stdin[:min( [ len(str_stdin), 4096])])
            str_stdin = str_stdin[min( [ len(str_stdin), 4096]):]
            read_from_child += 1
        elif popen_inst.tochild in wlist:
            popen_inst.tochild.close()

        #logging.debug("len(str_stdin) = %i, read_from_child = %i, rlist = %s, wlist = %s", len(str_stdin), read_from_child, rlist, wlist)
        if popen_inst.poll() != -1 and len(str_stdin) == 0 and (read_from_child == -1 or read_from_child == 0):
            break
    
    logging.debug("Exit code: %i", popen_inst.wait())
    logging.debug("stdout: %s", str_stdout)
    logging.debug("strerr: %s", str_stderr)
    return str_stdout, str_stderr


class AvailableGlideins(xml.sax.handler.ContentHandler):
    
    # Command to query the collector for available glideins
    command = "condor_status -avail -const '(IsUndefined(Offline) == True) || (Offline == false)' -format '<glidein name=\"%s\"/>' 'Name'"
    
    owner_idle = {}
    
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
            
            if not self.owner_idle.has_key(attributes[owner]):
                self.owner_idle[attributes[owner]] = 0
            self.owner_idle[attributes[owner]] += 1
            
    def GetOwnerIdle(self):
        return self.owner_idle


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
    
    command = "condor_status -const '(IsUndefined(IS_GLIDEIN) == FALSE) && (IS_GLIDEIN == TRUE) && (IsUndefined(Offline))' -format '<glidein name=\"%s\"/>' 'Name'"
    
    
    
    
