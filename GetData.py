# Used to copy given Jira project data to local drive
#
# 21.11.2019 mika.nokka1@gmail.com 
# 
# NOTES:
# 1) For this POC removed .netrc authetication, using pure arguments
#
# Traps worng JQL query and possible corrupted attachment case (not downloading corrupted fileS) 
# 
#
# Python V2
#
#from __future__ import unicode_literals

#import openpyxl 
import sys, logging
import argparse
#import re
from collections import defaultdict
from ChangeIssue import Authenticate  # no need to use as external command
from ChangeIssue import DoJIRAStuff

import glob
import re
import os
import time
import unidecode
from jira import JIRA, JIRAError
from collections import defaultdict
from time import sleep
import keyboard

start = time.clock()
__version__ = u"0.1"

# should pass via  parameters
#ENV="demo"
ENV=u"PROD"

logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    logging.debug (u"--Created date field copier starting --") 

 
    parser = argparse.ArgumentParser(description=" Copy Jira JQL result issues attachments to given directory",
    
    
    epilog="""
    
    EXAMPLE:
    
    GetData.py  -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -q \"project=TOP and attachments is NOT EMPTY\" -d TMPDIR"""

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-d', help='<Path for attachements downloading>, . by default',metavar="dirpath",default=".\\")
    parser.add_argument('-q', help='<JIRA JQL query for issues>',metavar="JQLquery")
    parser.add_argument('-r', help='<DryRun - do nothing but emulate. Off by default>',metavar="on|off",default="off")
 

    args = parser.parse_args()
       
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    JQL=args.q or ''
    if (args.r=="on"):
         SKIP=1
    else:
        SKIP=0    
    DIR=args.d
    #logging.info("DIR:{0}".format(DIR))
    #logging.info("SKIP:{0}".format(SKIP))
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' or JQL==''):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,JQL,DIR)



############################################################################################################################################
# Parse attachment files and add to matching Jira issue
#

#NOTE: Uses hardcoded sheet/column value

def Parse(JIRASERVICE,PSWD,USER,ENV,jira,SKIP,JQL,DIR):

    # Change these according the need, or add as program arguments
 
    #JQLQuery="project=TOP and attachments is NOT EMPTY"  # TODO: AS AN ARGUMENT 
   

    i=1      
    #SKIP --> DRYRUN=1 , real operation =0, TODO AS AN ARGUMENT
    try:
        
        #haku=jira.search_issues(JQL, fields="attachment", maxResults=2000)
        #logging.info("JQL haku:{0}".format(haku))
        
        #sys.exit(5)
        
        for issue in jira.search_issues(JQL, fields="attachment,issuetype", maxResults=2000): # TODO: MAX ISSUE AN AN ARGUMENT
            
                if (keyboard.is_pressed("x")):
                   logging.debug("x pressed, stopping now")
                   break
                #sleep(0.5)

                logging.debug("JQL QUERY:{0}".format(JQL))
                logging.debug("  issue.fields.attachment:{0}".format(issue.fields.attachment))
            

                logging.info("....... COUNTER:{0}...................................................................................".format(i))
                #TODO:BUG: if more than one match will fail
                myissuekey=format(issue.key)
                logging.info("Jira issue:{0}".format(myissuekey))
                #logging.debug("issue.fields.subtasks:{0}".format(issue.fields.subtasks))
                #logging.debug("issue.fields:{0}".format(issue.fields))
                #id=jira.issue.id
                #type=jira.issue_type(issue)
                #try:
                issuetype=issue.fields.issuetype
                logging.debug("issuetype:{0}".format(issuetype))
               
                
                #try
                if (str(issuetype)=="Task"):
                    logging.debug("----> TASK")
                elif (str(issuetype)=="Sub-task"):
                    logging.debug("----> SUBTASK")
                else:
                    logging.debug("----> UNKNOWN ISSUETYPE")
                
                #except AttributeError:
                #   logging.debug("attribute error")
                
                #logging.debug("issue.fields.parent:{0}".format(issue.fields.parent))
                #issue.fields.parent
                #for subtasks in issue.fields.subtasks:
                #    logging.debug("issue.fields.subtasks:{0}".format(subtasks))
                    
                # TODO: IF field info is needed to find out
                #logging.debug("ISSUE: {0}:".format(issue))
                #logging.debug("ID{0}: ".format(issue.id))
                #logging.debug("Jira issue field data (from Jira): {0}".format(issue.fields))
                #for field_name in issue.raw['fields']:
                   # print "Field:", field_name, "Value:", issue.raw['fields'][field_name]
                   #logging.debug("field nanme: {0}".format(field_name))
                #   value=issue.raw['fields'][field_name]
                #   if (str(value) != "None"):
                #       logging.debug("field: {0} Value: {1} ".format(field_name,value))
                
                
                KEY=str(issue.key)
                path=os.path.join(DIR,KEY)
                #logging.info("--> path:{0}".format(path))
           
                # Create target Directory if don't exist
                if not os.path.exists(path=os.path.join(DIR,KEY)):
                    if (SKIP==0):
                        os.mkdir(path)
                    else:
                        logging.info("!!! SIMULATED EXECUTION ONLY!!!")
                    logging.info("Created directory:{0}".format(KEY))
                else:    
                    logging.info("Directory:{0} exists. DID NOTHING".format(KEY))
                
                sikaissue = jira.issue(issue, expand="attachment") # worked originally also using just issue (not expanding)
                for attachment in sikaissue.fields.attachment:
                     logging.info("Attachment name: '{filename}', size: {size} ID:{ID}".format(filename=attachment.filename, size=attachment.size,ID=attachment.id))
                     item=""
                     try:
                         
                         kissa=jira.attachment(attachment.id)
                         #logging.info("kissa:{0}".format(kissa))
                         #item = attachment.get() # worked originally
                         item = kissa.get()
                        
                        
                         #logging.info("item:{0}".format(item))
                         jira_filename = attachment.filename   
                         path=os.path.join(DIR,KEY,jira_filename) 
                     
                         if (SKIP==0):
                            with open(path, 'wb') as file:        
                                file.write(item)
                        
                         else:
                             logging.info("!!! SIMULATED EXECUTION ONLY!!!")
                         logging.info("Writing directory:{0} File:{1} ".format(path,jira_filename)) 
                          
                     except Exception as error:
                               logging.error("*******************************************************************************************************************")
                               logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(error.status_code,error.text))         
                               logging.error("POSSIBLE CORRUPTED ATTACHEMENT:{0}. NOT DOWNLOADED".format(attachment))
                               logging.error("*******************************************************************************************************************")
                    
                
                i=i+1
                logging.debug("---------------------------------------------------------------")
    
    except JIRAError as e: 
            logging.error(" ********** JIRA ERROR DETECTED: ***********")
            logging.error(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
            logging.error(" ********** Maybe it's the JQL query:  {0}".format(JQL))
            if (e.status_code==400):
                logging.error("400 error dedected") 
    else:
        logging.info("All OK")
  
        
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
        

 
  

    
logging.debug ("--Python exiting--")
if __name__ == "__main__":
    main(sys.argv[1:]) 