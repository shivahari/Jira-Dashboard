"""
This script will plot the arrival times of tickets into the 'In QA' status
For now, we are using the public JIRA repository of secondlife:
https://jira.secondlife.com

I am choosing to write a functional script with no classes for now. Hey, Hackathon and all that you know!

"""

from jira import JIRA
import arrow, time, json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import credentials as secret

JIRA_URL = secret.JIRA_URL
JIRA_PROJECT = secret.PROJECT


def get_queue_arrival_times(state,last_n_days=30):
    "Get the arrival times of a queue"
    jira_options = {'server': JIRA_URL}
    jira = JIRA(jira_options, basic_auth=(secret.USERNAME,secret.PASSWORD))
    ticket_list = jira.search_issues('project="%s" AND updated > -%sd ORDER BY priority DESC'%(JIRA_PROJECT,str(last_n_days)))
    print '- Fetched all tickets in for Project %s that were updated in the last %s days'%(JIRA_PROJECT,str(last_n_days))
    arrival_queue = []
    for ticket in ticket_list:
        issue = jira.issue(ticket.key,expand='changelog')
        for action in issue.changelog.histories:
            for item in action.items:
                if item.toString == state:
                    arrival_queue.append(action.created)
    
    return arrival_queue


def plot_arrival_dates(raw_arrival_times):
    "Plot the arrival dates"
    #2. Plot the times
    #Make this dumb for now
    raw_arrival_dates = [date.split('T')[0] for date in raw_arrival_times]
    arrival_dates = []
    for iso_date in raw_arrival_times:
        my_date = arrow.get(iso_date.split('T')[0])
        arrival_dates.append(my_date.naive)
    time_delta = max(arrival_dates) - min(arrival_dates)
    num_days =  int(time_delta.days)
    x_points = [max(arrival_dates) - timedelta(days=x) for x in range(-1,num_days+1)]

    y_points = []
    for date in x_points:
        count = 0
        temp_date = date.strftime('%Y-%m-%d')
        if temp_date in raw_arrival_dates:
            y_points.append(1)
        else:
            y_points.append(0)

    rows = [(x,y) for x,y in zip(x_points,y_points)]
    
    x_points = [date.strftime('%Y-%m-%d') for date in x_points]
    json_data = {"x_axis":x_points,"y_axis":y_points}
    json_data = "arrivalData = '" + json.dumps(json_data) + "';"
    with open('qa_arrival.json','w') as outfile:
        outfile.write(json_data)

    return


def run_queue_arrival_analysis(state,last_n_days=30):
    "Produce arrival queue statistics for a given state"
    #1. Get the arrival times into the state
    raw_arrival_times = get_queue_arrival_times(state,last_n_days)
    print '-Got the arrival times for the queue state: %s'%state
    print '----Queue arrival times for %s: '%state,raw_arrival_times

    plot_arrival_dates(raw_arrival_times)
    print '-Plotted the arrival queue for %s'%state


def run_qa_queue_arrival_analysis(last_n_days=30):
    "Plot data about when a ticket transitions into the 'In QA' status"
    run_queue_arrival_analysis('Feature Test',last_n_days=last_n_days)


#----START OF SCRIPT
if __name__=='__main__':
    print 'Script started'
    run_qa_queue_arrival_analysis(15)
