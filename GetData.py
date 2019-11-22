# Used to copy given Jira project data to local drive
#
# 21.11.2019 mika.nokka1@gmail.com 
# 
# NOTES:
# 1) For this POC removed .netrc authetication, using pure arguments
# 2) JQL query for chosen isseus: JQLQuery="project=xxxxx"  (incoded)
# 3) SKIP variable for possible dry run
# 
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

start = time.clock()
__version__ = u"0.1"

# should pass via  parameters
#ENV="demo"
ENV=u"PROD"

logging.basicConfig(level=logging.INFO) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    logging.debug (u"--Created date field copier starting --") 

 
    parser = argparse.ArgumentParser(description=" Copy Jira JQL result issues attachments to given directory",
    
    
    epilog=" --TBD--- "

    
    )
    
   

    #parser = argparse.ArgumentParser(description="Copy Jira JQL result issues' attachments to given directory")
    
    #parser = argparse.ArgumentParser(epilog=" not displayed ") # TODO: not working
    
    parser.add_argument('-v', help='Show version&author and exit', action='version',version="Version:{0}   mika.nokka1@gmail.com ,  MIT licenced ".format(__version__) )
    
    parser.add_argument("-w",help='<JIRA password>',metavar="password")
    parser.add_argument('-u', help='<JIRA user account>',metavar="user")
    parser.add_argument('-s', help='<JIRA service>',metavar="server_address")
    parser.add_argument('-d', help='<Target directory path for attachements download>',metavar="dirpath")
    parser.add_argument('-q', help='<JIRA JQL query for issues>',metavar="JQLquery")
    parser.add_argument('-r', help='<DryRun - do nothing>')
    #parser.add_argument('-p','--project', help='<JIRA project>')
 

    args = parser.parse_args()
    
    #if args.version:
    #    print ("Tool . version: %s"  % __version__)
    #    sys.exit(2)    
           
    #filepath = args.filepath or ''
    
    JIRASERVICE = args.s or ''
    PSWD= args.w or ''
    USER= args.u or ''
    #RENAME= args.rename or ''
    #ASCII=args.ascii or ''
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' ):
        logging.error("\n---> MISSING ARGUMENTS!!\n ")
        parser.print_help()
        sys.exit(2)
        
     
    Authenticate(JIRASERVICE,PSWD,USER)
    jira=DoJIRAStuff(USER,PSWD,JIRASERVICE)
    
    Parse(JIRASERVICE,JIRAPROJECT,PSWD,USER,ENV,jira)



############################################################################################################################################
# Parse attachment files and add to matching Jira issue
#

#NOTE: Uses hardcoded sheet/column value

def Parse(JIRASERVICE,JIRAPROJECT,PSWD,USER,ENV,jira):

    # Change these according the need, or add as program arguments
    JIRAPROJECT="TOP"
    JQLQuery="project=TOP and attachments is NOT EMPTY"  # TODO: AS AN ARGUMENT 

    i=1      
    SKIP=1 # DRYRUN=1 , real operation =0, TODO AS AN ARGUMENT
    for issue in jira.search_issues(JQLQuery, fields="attachment", maxResults=200): # TODO: MAX ISSUE AN AN ARGUMENT

                logging.info("...................................................................................")
                #TODO:BUG: if more than one match will fail
                myissuekey=format(issue.key)
                logging.info("Jira project: {0}  Issue:{1}".format(JIRAPROJECT,myissuekey))
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
                # Create target Directory if don't exist
                if not os.path.exists(KEY):
                    os.mkdir(KEY)
                    logging.info("Created directory:{0}".format(KEY))
                else:    
                    logging.info("Directory:{0} exists. DID NOTHING".format(KEY))
                
                for attachment in issue.fields.attachment:
                     logging.info("Attachment name: '{filename}', size: {size} ID:{ID}".format(filename=attachment.filename, size=attachment.size,ID=attachment.id))
                     item = attachment.get()    
                     jira_filename = attachment.filename   
                     path=os.path.join(KEY,jira_filename) 
                     logging.info("Writing directory:{0} File:{1} ".format(path,jira_filename))
                     with open(path, 'w') as file:        
                         file.write(item) 
                
                if (SKIP==0):
                    #sys.exit(5)  #to be sure not to doit first time
                    try:
                        #issue.update(fields={SourceCustomFieldString: int(TargetCustomField)})  #TODO:ARGUMENT
                        issue.update(fields={TargetCustomFieldString: SourceFieldValue})  #TODO:ARGUMENT
                        logging.debug("*** Copy operation done***")
                        time.sleep(0.7) # prevent jira crashing for script attack
                    except JIRAError as e: 
                        logging.debug(" ********** JIRA ERROR DETECTED: ***********")
                        logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                    #sys.exit(5) 
                    else: 
                        logging.debug("All OK")
                    #sys.exit(5)
                else:
                    logging.debug("SKIPPED ACTIONS. DRYRUN ONLY")
                
                i=i+1
                logging.debug("---------------------------------------------------------------")


    
    
  
        
    end = time.clock()
    totaltime=end-start
    print ("Time taken:{0} seconds".format(totaltime))
       
            
    print ("*************************************************************************")
        

 
  

    
logging.debug ("--Python exiting--")
if __name__ == "__main__":
    main(sys.argv[1:]) 