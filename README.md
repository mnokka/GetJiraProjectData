# GetJiraProjectData



Fetches given Jira JQL query (matching) issues' attachments to given directory



Traps error cases

1) JQL error

2) Corrupted attachment (skips downloading)



## USAGE:

  -h, --help         show this help message and exit
  
  -v                 Show version&author and exit
  
  -w password        <JIRA password>
  
  -u user            <JIRA user account>
  
  -s server_address  <JIRA service>
  
  -d dirpath         <Path for attachements downloading>, . by default
  
  -q JQLquery        <JIRA JQL query for issues>
  
  -r on|off          <DryRun - do nothing but emulate. Off by default>
  
  
  

## EXAMPLES:


GetData.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -q "project=TOP and attachments is NOT EMPTY" -d TMPDIR\ZZZ


GetData.py -u MYUSERNAME -w MYPASSWORD -s https://MYOWNJIRA.fi/ -q "project=TOP and attachments is NOT EMPTY" -d .
  

Uses Python V2
