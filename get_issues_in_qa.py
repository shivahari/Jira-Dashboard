"""
This script will plot:
a) how long a ticket spent in the 'In Testing' state
"""

from ConnectJira import ConnectJira
import credentials as secret


#----START OF SCRIPT
if __name__=='__main__':
    print 'Script started'
    obj = ConnectJira(secret.JIRA_URL,
                      secret.PROJECT,
                      secret.USERNAME,
                      secret.PASSWORD)
    status = "Feature Test"
    print 'About to search for issues in status: %s'%status
    print 'If that looks wrong, please edit the file %s)'%__file__
    obj.get_issues_in_qa(status)
    print 'Please open the file in_qa_status.html to see your data'
