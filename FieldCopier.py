# Used to copy values from one custom field to another
#
# 18.3.2019 mika.nokka1@gmail.com 
# 
# NOTE: For this POC removed .netrc authetication, using pure arguments
# JQL query for chosen isseus: JQLQuery="project=NRP"  (incode)
#
# Source and custom field in code
# SourceCustomField=issue.fields.customfield_10019  #TODO:ARGUMENT
# TargetCustomField=issue.fields.customfield_10019  #TODO:ARGUMENT 
#
#from __future__ import unicode_literals

import openpyxl 
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

logging.basicConfig(level=logging.DEBUG) # IF calling from Groovy, this must be set logging level DEBUG in Groovy side order these to be written out



def main(argv):
    
    JIRASERVICE=u""
    JIRAPROJECT=u""
    PSWD=u''
    USER=u''
  
    logging.debug (u"--Custom field copier starting --") 

 
    parser = argparse.ArgumentParser(usage="""
    {1}    Version:{0}     -  mika.nokka1@gmail.com
    
    USAGE:
    ---password | -w <JIRA password>
    --service   | -s <JIRA service>
    --user   | -u <JIRA user>

    """.format(__version__,sys.argv[0]))

   
    parser.add_argument('-v','--version', help='<Version>', action='store_true')
    
    parser.add_argument('-w','--password', help='<JIRA password>')
    parser.add_argument('-u','--user', help='<JIRA user>')
    parser.add_argument('-s','--service', help='<JIRA service>')
    #parser.add_argument('-p','--project', help='<JIRA project>')
 
        
    args = parser.parse_args()
    
    if args.version:
        print 'Tool version: %s'  % __version__
        sys.exit(2)    
           
    #filepath = args.filepath or ''
    
    JIRASERVICE = args.service or ''
    PSWD= args.password or ''
    USER= args.user or ''
    #RENAME= args.rename or ''
    #ASCII=args.ascii or ''
    
    # quick old-school way to check needed parameters
    if (JIRASERVICE=='' or  PSWD=='' or USER=='' ):
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
    JQLQuery="project=NRP"  # TODO: ARGUMENT

    i=1      
    SKIP=0
    for issue in jira.search_issues(JQLQuery, maxResults=10):

                #TODO:BUG: if more than one match will fail
                myissuekey=format(issue.key)
                logging.debug("Jira issue key (from Jira): {0}".format(myissuekey))
                #logging.debug("ISSUE: {0}:".format(issue))
                #logging.debug("ID{0}: ".format(issue.id))

                # Change these according the need, or add as program arguments
                SourceCustomField=issue.fields.customfield_14204  #TODO:ARGUMENT
                TargetCustomField=issue.fields.customfield_14350  #TODO:ARGUMENT  
               
                
                logging.debug("Source custom field value: {0}".format(SourceCustomField))
                logging.debug("Target custom field value: {0}".format(TargetCustomField))
                if (SourceCustomField is None):
                    logging.debug("*** No source custom field value . Skipping copy operation ****")
                    SKIP=1
                else:
                    SKIP=0
                    logging.debug("{0}: Going to copy {1} ----> {2}".format(i,SourceCustomField,TargetCustomField))
                if (TargetCustomField is None):
                    logging.debug("*** No target custom field value  ****")    
                    
               
                
             
                #issue.update(customfield_10019=DrawingNumber   , single test field)
                
                
                if (SKIP==0):
                    #sys.exit(5)  #to be sure not to doit first time
                    try:
                        #issue.update(fields={SourceCustomField: TargetCustomField})  #TODO:ARGUMENT
                        logging.debug("try phase")
                    except JIRAError as e: 
                        logging.debug(" ********** JIRA ERROR DETECTED: ***********")
                        logging.debug(" ********** Statuscode:{0}    Statustext:{1} ************".format(e.status_code,e.text))
                    #sys.exit(5) 
                    else: 
                        logging.debug("All OK")
                    #sys.exit(5)
                
                
                i=i+1
                logging.debug("---------------------------------------------------------------")


    
    
  
        
    end = time.clock()
    totaltime=end-start
    print "Time taken:{0} seconds".format(totaltime)
       
            
    print "*************************************************************************"
        

 
  

    
logging.debug ("--Python exiting--")
if __name__ == "__main__":
    main(sys.argv[1:]) 