""""
This script will plot:
a) the average number of words each JIRA user puts in their description
Very useful to spot the vague ones!
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
    print 'About to figure out the average words each user puts in their description'
    obj.get_description_reporters_data_frame()
    print 'Please open the file description_average_words.html to see your data'
