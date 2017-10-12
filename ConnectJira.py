"""
Connect to Jira server and get the issue in QA
"""

from jira import JIRA
import json
import numpy as np
import pandas as pd
import re
import arrow

class ConnectJira():
    """
    Connect Jira class to connect to establish connections
    """
    
    def __init__(self,server,project_name):
        self.jira_obj = JIRA(server)
        self.project = project_name
        

    def get_issues_in_qa(self):
        "Get the issues"
        issue_dict = {}
        issues = self.jira_obj.search_issues("'project'='%s' AND status = 'In QA'"%self.project)
        for issue in issues:
            ticket = self.jira_obj.issue(issue.key,expand='changelog')
            for action in ticket.changelog.histories:
                for item in action.items:
                    if item.field == 'status':
                        if item.toString == 'In QA':
                            #2013-04-18T10:18:23.428-0500
                            #time = re.search('(?P<date>\d{4}[-]\d{2}[-]\d{2})T(?P<time>\d{2}[:]\d{2}[:]\d{2})*',action.created)
                            #print ticket,item.toString,time.group('date'),time.group('time')
                            da_update_date = action.created
                            now_date = arrow.now()
                            ticket_in_qa_time = now_date - arrow.get(da_update_date)
                            print ticket,item.toString,ticket_in_qa_time


if __name__ == '__main__':
    obj = ConnectJira('https://jira.secondlife.com','SUN')
    obj.get_issues_in_qa()


        
    
    




            














