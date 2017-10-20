""""
This script will plot:
a) the most worked on component in the last 'N' days
Very useful to spot the quiet ones!
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
    num_days = 30
    print 'About to figure out the most worked components in the last %d days'%num_days
    print 'If that sounds wrong, please edit the file %s'%__file__
    obj.get_components(num_days)
    print 'Please open the file most-worked-components.html to see your data'
