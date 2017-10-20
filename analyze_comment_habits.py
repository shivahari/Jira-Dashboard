""""
This script will plot:
a) the average number of words each JIRA user puts in their comments
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
    print 'About to figure out the average words each user puts in their comments'
    obj.get_comments()
    print 'Please open the file average_involvement.html to see your data'
