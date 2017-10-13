"""
Connect to Jira server and get the issue in QA
"""

from jira import JIRA
import json
import numpy as np
import pandas as pd
import re
import arrow
import matplotlib.pyplot as plt
from time import strftime

class ConnectJira():
    """
    Connect Jira class to connect to establish connections
    """
    
    def __init__(self,server,project_name):
        self.jira_obj = JIRA(server)
        self.project = project_name
        

    def get_issues_in_qa(self):
        "Get the issues"
        status_qa_data_frame = pd.DataFrame(columns=['ticket-ID','status','days'])
        issues = self.jira_obj.search_issues("'project'='%s' AND status = 'In QA'"%self.project)
        for issue in issues:
            ticket = self.jira_obj.issue(issue.key,expand='changelog')
            for action in ticket.changelog.histories:
                for item in action.items:
                    if item.field == 'status':
                        if item.toString == 'In QA':
                            da_update_date = action.created
                            now_date = arrow.now()
                            ticket_in_qa_time = now_date - arrow.get(da_update_date)
                            ticket_in_qa_time = int(ticket_in_qa_time.days)
                            status_qa_data_frame.loc[len(status_qa_data_frame)] = {'ticket-ID':ticket.key,'status':item.toString,'days':ticket_in_qa_time}
        self.status_qa_data_frame = status_qa_data_frame
        print self.status_qa_data_frame
        json_data = {"x_axis":list(self.status_qa_data_frame['ticket-ID']),"y_axis":list(self.status_qa_data_frame['days'])}
        json_data = "get_issue = '" + json.dumps(json_data) + "';"
        with open('get_issue_in_qa.json','w') as outfile:
            outfile.write(json_data)


    def get_reporter_list(self):
        "Get the list of JIRA ticket reporters"
        #reporter_list_data_frame = 
        reporter_list = []
        tickets= self.jira_obj.search_issues("'project'='%s'"%self.project)
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            reporter = issue.fields.reporter.name 
            reporter_list.append(reporter)

        return reporter_list


    def get_description_reporters_data_frame(self):
        "Get a dataframe of reporters and words used in description"
        reporter_list = self.get_reporter_list()
        verbose_data_frame = pd.DataFrame(columns=['name','avg_word_count'])
        for reporter in reporter_list:
            tickets = self.jira_obj.search_issues("'project'='%s' AND 'reporter'='%s'"%(self.project,reporter))
            total_word_count = []
            for ticket in tickets:
                issue = self.jira_obj.issue(ticket.key)
                if issue.fields.reporter.name == reporter:
                    des_word_count =  issue.fields.description.split(' ')
                    total_word_count.append(len(des_word_count))
            if total_word_count > 0:
                avg_words = np.average(total_word_count)
                verbose_data_frame.loc[len(verbose_data_frame)] = {'name':reporter,'avg_word_count':avg_words}
        self.verbose_data_frame = verbose_data_frame
        print self.verbose_data_frame
        json_data = {"x_axis":list(self.verbose_data_frame['name']),"y_axis":list(self.verbose_data_frame['avg_word_count'])}
        json_data = "desc_word_count = '" + json.dumps(json_data) + "';"
        with open('description_word_count.json','w') as outfile:
            outfile.write(json_data)


    def get_comments(self):
        "Get the comments"
        reporter_list = []
        tickets= self.jira_obj.search_issues("'project'='%s'"%self.project)
        comment_authors = []
        comment_authors_data_frame = pd.DataFrame(columns=['name','comment_word_count','no_times'])
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            for item in issue.fields.comment.comments:
                comment_authors_data_frame.loc[len(comment_authors_data_frame)] = {'name':item.author.name,'comment_word_count':len(item.body.split(' ')),'no_times':1}
        unique_comment_authors_data_frame =  comment_authors_data_frame.groupby(['name']).sum()
        unique_comment_authors_data_frame['average'] = unique_comment_authors_data_frame['comment_word_count'] / (unique_comment_authors_data_frame['no_times']*1.0)
        self.unique_comment_authors_data_frame = unique_comment_authors_data_frame
        print self.unique_comment_authors_data_frame 
        json_data = {"x_axis":self.unique_comment_authors_data_frame.index.tolist(),"y_axis":list(self.unique_comment_authors_data_frame['average'])}
        json_data = "comm_word_count = '" + json.dumps(json_data) + "';"
        with open('comment_word_count.json','w') as outfile:
            outfile.write(json_data)


    def plot_graph(self,x_points,y_points):
        "Plot Graph using the X and Y axis passed"
        plt.plot(x_points,y_points)
        plt.show()


if __name__ == '__main__':
    obj = ConnectJira('https://jira.secondlife.com','SUN')
    obj.get_issues_in_qa()
    obj.get_description_reporters_data_frame()
    obj.get_comments()


        
    
    




            














