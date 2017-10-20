"""
Connect to JIRA server and get data 
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
    
    def __init__(self,server,project_name,username,password):
        jira_options = {'server': server}
        self.jira_obj = JIRA(jira_options, basic_auth=(username,password))
        self.project = project_name


    def get_issues_in_qa(self,status_string):
        "Get the issues"
        status_qa_data_frame = pd.DataFrame(columns=['ticket-ID','status','days'])
        issues = self.jira_obj.search_issues("'project'='%s' AND status = '%s' AND updated > -30d"%(self.project,status_string))
        for issue in issues:
            ticket = self.jira_obj.issue(issue.key,expand='changelog')
            for action in ticket.changelog.histories:
                for item in action.items:
                    if item.field == 'status':
                        if item.toString == status_string:
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
        tickets= self.jira_obj.search_issues("'project'='%s' AND updated > -30d"%self.project)
        print "Number of tickets that match the filter:",len(tickets)
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            reporter = issue.fields.reporter.name 
            reporter_list.append(reporter)

        return reporter_list


    def get_description_reporters_data_frame(self):
        "Get a dataframe of reporters and words used in description"
        #reporter_list = self.get_reporter_list()
        verbose_data_frame = pd.DataFrame(columns=['name','total_word_count','no_times'])
        tickets= self.jira_obj.search_issues("'project'='%s' AND updated > -30d"%self.project)
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            total_word_count = 0
            reporter = issue.fields.reporter.name
            if issue.fields.description is not None:
                total_word_count =  len(issue.fields.description.split(' '))
            verbose_data_frame.loc[len(verbose_data_frame)] = {'name':reporter,'total_word_count':total_word_count,'no_times':1}
        unique_verbose_data_frame = verbose_data_frame.groupby(['name']).sum()
        unique_verbose_data_frame['average'] = unique_verbose_data_frame['total_word_count']/(unique_verbose_data_frame['no_times']*1.0)
        self.verbose_data_frame = unique_verbose_data_frame
        print self.verbose_data_frame
        json_data = {"x_axis":self.verbose_data_frame.index.tolist(),"y_axis":list(self.verbose_data_frame['average'])}
        json_data = "desc_word_count = '" + json.dumps(json_data) + "';"
        with open('description_word_count.json','w') as outfile:
            outfile.write(json_data)


    def get_comments(self):
        "Get the comments"
        reporter_list = []
        tickets= self.jira_obj.search_issues("'project'='%s' AND updated > -30d"%self.project)
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


    def get_components(self,days=30):
        "Get all the components worked on in a given timeframe"
        tickets= self.jira_obj.search_issues("'project'='%s' AND updated > -%sd"%(self.project,str(days)))
        components_data_frame = pd.DataFrame(columns=['name','no_times'])
        for ticket in tickets:
            issue = self.jira_obj.issue(ticket.key)
            if len(issue.fields.components):
                for component in issue.fields.components:
                    components_data_frame.loc[len(components_data_frame)] = {'name':component.name,'no_times':1}
        self.unique_components_data_frame = components_data_frame.groupby(['name']).sum()
        print self.unique_components_data_frame
        json_data = {"x_axis":self.unique_components_data_frame.index.tolist(),"y_axis":list(self.unique_components_data_frame['no_times'])}
        json_data = "component_count = '" + json.dumps(json_data) + "';"
        with open('component_count.json','w') as outfile:
            outfile.write(json_data)


    def plot_graph(self,x_points,y_points):
        "Plot Graph using the X and Y axis passed"
        plt.plot(x_points,y_points)
        plt.show()


