# JiraFieldCopier

Copy custom field1 (source) values to custom field2 (target)

The source custom field and target custom field must exist in system (normally target is empty and waits for this copying)

NOTE: JQL query for issues and source and target field's IDs defined in code
NOTE: This example copies values from int field --> string field


USAGE:

FieldCopier.py -s https://THEJIRA.COM -u USER -w PASSWORD


   ---password | -w <JIRA password>
  
   --service   | -s <JIRA service>
    
   --user   | -u <JIRA user>


NOTE: Before inhouse tool usage, one might first check if ScriptRunner supports wished field->field conversion.  (https://scriptrunner.adaptavist.com/latest/jira/builtin-scripts.html#_copy_custom_field_values ) . 
