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
        status_qa_data_frame = pd.DataFrame(columns=['Ticket-ID','Status','Days'])
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
                            status_qa_data_frame.loc[len(status_qa_data_frame)] = {'Ticket-ID':ticket.key,'Status':item.toString,'Days':ticket_in_qa_time.days}
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
        verbose_data_frame = pd.DataFrame(columns=['Reporter','Avg_word_count'])
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
                verbose_data_frame.loc[len(verbose_data_frame)] = {'Reporter':reporter,'Avg_word_count':avg_words}
        self.verbose_data_frame = verbose_data_frame
        #self.plot_graph(verbose_data_frame['Reporter'],verbose_data_frame['Avg_word_count'])
        
        print verbose_data_frame

    def get_comments(self):
        "Get the comments"
        reporter_list = []
        tickets= self.jira_obj.search_issues("'project'='%s'"%self.project)
        comment_authors = []
        comment_authors_data_frame = pd.DataFrame(columns=['Author_name','Comment_word_count','No_times'])
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            for item in issue.fields.comment.comments:
                comment_authors_data_frame.loc[len(comment_authors_data_frame)] = {'Author_name':item.author.name,'Comment_word_count':len(item.body.split(' ')),'No_times':1}
        unique_comment_authors_data_frame =  comment_authors_data_frame.groupby(['Author_name']).sum()
        unique_comment_authors_data_frame['Average'] = unique_comment_authors_data_frame['Comment_word_count'] / (unique_comment_authors_data_frame['No_times']*1.0)
        self.unique_comment_authors_data_frame = unique_comment_authors_data_frame
        print self.unique_comment_authors_data_frame 


    def plot_graph(self,x_points,y_points):
        "Plot Graph using the X and Y axis passed"
        plt.plot(x_points,y_points)
        plt.show()

if __name__ == '__main__':
    obj = ConnectJira('https://jira.secondlife.com','SUN')
    #obj.get_issues_in_qa()
    #obj.get_description_reporters_data_frame()
    obj.get_comments()


        
    
    




            














