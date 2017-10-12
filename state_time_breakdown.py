"""
This script will plot:
a) how long a ticket spent in each state
b) who all collaborated on the ticket

For now, we are using the public JIRA repository of secondlife:
https://jira.secondlife.com

I am choosing to write a functional script with no classes for now. Hey, Hackathon and all that you know!

WARNING: I could not complete plotting the graph. I did retrieve the information and it looks good
"""

from jira import JIRA
import arrow, time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

JIRA_URL = 'https://jira.secondlife.com'
JIRA_PROJECT = 'SUN'


def fetch_tickets(last_n_days=30):
    "Fetch the tickets updated in the last n days"
    pass


def get_state_time_information(last_n_days=30):
    "Get the state time information for each of the tickets"
    jira = JIRA(JIRA_URL)
    ticket_list = jira.search_issues('project=%s AND updated > -%sd ORDER BY priority DESC'%(JIRA_PROJECT,str(last_n_days)))
    print '- Fetched %d tickets in for Project %s that were updated in the last %s days'%(len(ticket_list),JIRA_PROJECT,str(last_n_days))

    #Create a data structure which is a list of tuples like (ticket key,status,assignee,time)
    status_assignee_time = []

    for ticket in ticket_list:
        issue = jira.issue(ticket.key,expand='changelog')
        #Prepare to find changes in the items of the histories data structure
        prev_status = ''
        current_status = ''
        prev_assignee = 'Unassigned'
        current_assignee = 'Unassigned'
        prev_action_time = 0

        for action in issue.changelog.histories:
            current_action_time = arrow.get(action.created) 
            for item in action.items:
                if item.field == 'status':
                    current_status = item.toString
                if item.field == 'assignee':
                    current_assignee = item.toString
            #Update the row only if either assignee or status change
            if current_status != prev_status or current_assignee != prev_assignee:
                time_spent = current_action_time - prev_action_time if prev_action_time != 0 else current_action_time - current_action_time
                status_assignee_time.append((ticket.key,current_status,current_assignee,time_spent))
                if current_assignee != prev_assignee:
                    prev_assignee = current_assignee
                if current_status != prev_status:
                    prev_status = current_status
                prev_action_time = current_action_time

    return status_assignee_time



def run_state_time_analysis(last_n_days=30):
    "Get how long each ticket spent in which state"
    raw_state_time_information = get_state_time_information(last_n_days)
    print '--------'
    for row in raw_state_time_information:
        print '  ',row
    print '--------'


#----START OF SCRIPT
if __name__=='__main__':
    print 'Script started'
    run_state_time_analysis(1500)
