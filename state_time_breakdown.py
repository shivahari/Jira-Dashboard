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
import arrow, time, json
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

    #Create a data structure which is a list of lists like [ticket key,status,assignee,time]
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
                if len(status_assignee_time)>0:
                    status_assignee_time[-1][-1] = time_spent
                status_assignee_time.append([ticket.key,current_status,current_assignee,current_action_time - current_action_time])
                if current_assignee != prev_assignee:
                    prev_assignee = current_assignee
                if current_status != prev_status:
                    prev_status = current_status
                prev_action_time = current_action_time

    return status_assignee_time

def convert_timedelta(duration):
    "Src: https://stackoverflow.com/questions/14190045/how-to-convert-datetime-timedelta-to-minutes-hours-in-python"
    days, seconds = duration.days, duration.seconds
    days = days + seconds/(3600*24)

    return days

def run_state_time_analysis(last_n_days=30):
    "Get how long each ticket spent in which state"
    raw_state_time_information = get_state_time_information(last_n_days)
    #Figure out unique states and tickets
    unique_states = []
    unique_tickets = []
    for row in raw_state_time_information:
        if row[1] not in unique_states and row[1] != '':
            unique_states.append(row[1])
        if row[0] not in unique_tickets and row[0] != '':
            unique_tickets.append(row[0])
        
    print 'The %d unique states are: '%len(unique_states),unique_states
    print 'The %d unique tickets are: '%len(unique_tickets),unique_tickets

    my_super_data_structure = []
    #This is hell ~19 hours into the Hackathon
    for ticket in unique_tickets:
        state_delta_row = []
        for state in unique_states:
            delta = 0
            for row in raw_state_time_information:
                if row[1]==state and row[0]==ticket:
                    delta = convert_timedelta(row[3])
                    break
            state_delta_row.append(delta)
        my_super_data_structure.append(state_delta_row)

    my_super_data_structure = [list(x) for x in zip(*my_super_data_structure)] 
    #Form the freaking JSON for Highcharts
    series_data = []
    for i,state in enumerate(unique_states):
        state_json = {'name':state,'data':my_super_data_structure[i]}
        series_data.append(state_json)
    json_data = {'tickets':unique_tickets,'series':series_data}    
    
    json_data = "stateTimeData = '" + json.dumps(json_data) + "';"
    with open('state_time_breakdown.json','w') as outfile:
        outfile.write(json_data)

    return json_data

    



#----START OF SCRIPT
if __name__=='__main__':
    print 'Script started'
    run_state_time_analysis(1500)
