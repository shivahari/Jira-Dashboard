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
                            print ticket,item.toString,ticket_in_qa_time
                            status_qa_data_frame.loc[len(status_qa_data_frame)] = {'ticket-ID':ticket.key,'status':item.toString,'days':ticket_in_qa_time.days}
        self.status_qa_data_frame = status_qa_data_frame
        print self.status_qa_data_frame

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
        #self.plot_graph(verbose_data_frame['Reporter'],verbose_data_frame['Avg_word_count'])
        
        #print verbose_data_frame

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
        #print pd.merge(self.verbose_data_frame,self.unique_comment_authors_data_frame,on='name',how='right')


    def plot_graph(self,x_points,y_points):
        "Plot Graph using the X and Y axis passed"
        plt.plot(x_points,y_points)
        plt.show()

if __name__ == '__main__':
    obj = ConnectJira('https://jira.secondlife.com','SUN')
    obj.get_issues_in_qa()
    obj.get_description_reporters_data_frame()
    obj.get_comments()


        
    
    




            














