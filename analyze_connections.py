"""
This script will plot:
a) gather everyone who worked on a ticket (reporter, assignee or commenter)
b) plot a graph for how the connections look over a large number of tickets

For now, we are using the public JIRA repository of secondlife:
https://jira.secondlife.com

I am choosing to write a functional script with no classes for now. Hey, Hackathon and all that you know!

"""

from jira import JIRA
import arrow, time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import networkx as nx
import credentials as secret

JIRA_URL = secret.JIRA_URL
JIRA_PROJECT = secret.PROJECT


def get_collaboration_information(last_n_days=30):
    "Get the state time information for each of the tickets"
    jira_options = {'server': JIRA_URL}
    jira = JIRA(jira_options, basic_auth=(secret.USERNAME,secret.PASSWORD))
    ticket_list = jira.search_issues('project="%s" AND updated > -%sd ORDER BY priority DESC'%(JIRA_PROJECT,str(last_n_days)))
    print '- Fetched %d tickets in for Project %s that were updated in the last %s days'%(len(ticket_list),JIRA_PROJECT,str(last_n_days))

    #Create a data structure which is a list of lists like ['employee 1','employee 2',...]
    collaborator_master_list = []


    for ticket in ticket_list:
        issue = jira.issue(ticket.key,expand='changelog')
        collaborator_list = []
        #Add the reporter
        collaborator_list.append(issue.fields.reporter.name)

        #Add all the commenters
        for comment in issue.fields.comment.comments:
            collaborator_list.append(comment.author.name)

        #Prepare to find changes in the assignee
        prev_assignee = 'Unassigned'
        current_assignee = 'Unassigned'

        for action in issue.changelog.histories:
            for item in action.items:
                if item.field == 'assignee':
                    current_assignee = item.toString
            #Update the row only if assignee changed
            if current_assignee != prev_assignee:
                collaborator_list.append(current_assignee)
                prev_assignee = current_assignee

        #Make the collaborators unique, remove the 'None' entries and add them to the master list
        collaborator_list = list(set(collaborator_list))
        collaborator_list = [name for name in collaborator_list if name!=None]
        collaborator_master_list.append(collaborator_list)

    return collaborator_master_list


def plot_collaboration_data(collaboration_data):
    "Plot a weighted network graph of the raw collaboration information"

    #Figure out the unique users
    unique_users = []
    for ticket_collaboration_data in collaboration_data:
        for collaborator in ticket_collaboration_data:
            if collaborator not in unique_users:
                unique_users.append(collaborator)
    unique_users.sort()
    print '%d unique users:'%len(unique_users),unique_users

    #Create a graph with zero weight
    #It looks like a list of [user 1, user 2, weight]
    my_graph_data = [] 
    for i,user1 in enumerate(unique_users):
        for user2 in unique_users[i+1:]:
            my_graph_data.append([user1,user2,0])

    #Loop through the collaboration data and update the weights in my_graph_data
    #Every time a pair of users appear in the data, increase their weight by 1
    for ticket_collaboration_data in collaboration_data:
        ticket_collaboration_data.sort()
        for i,user1 in enumerate(ticket_collaboration_data):
            for user2 in ticket_collaboration_data[i+1:]:
                for node in my_graph_data:
                    if node[0] == user1 and node[1] == user2:
                        node[2] += 1

    #Yay! The data is ready for adding a graph
    G = nx.Graph()
    for user1,user2,weight in my_graph_data:
        G.add_edge(user1,user2,weight=weight)

    #Draw the nodes
    pos=nx.circular_layout(G) 
    nx.draw_networkx_nodes(G,pos,node_color='brown',node_size=200)
    
    all_weights = []
    all_nodes = []
    for (u,v,d) in G.edges(data=True):
        all_weights.append(d['weight']) #we'll use this when determining edge thickness
        all_nodes.append(u) #we'll use this when labeling nodes
        all_nodes.append(v) #we'll use this when labeling nodes
    unique_weights = list(set(all_weights))
    unique_nodes = list(set(all_nodes))
    print 'Unique weights are: ',unique_weights
    print 'Unique nodes are: ',unique_nodes
    for weight in unique_weights:
        weighted_edges = [(node1,node2) for (node1,node2,edge_attr) in G.edges(data=True) if edge_attr['weight']==weight]
        #I think multiplying by [num_nodes/sum(all_weights)] makes the graphs edges look cleaner
        nx.draw_networkx_edges(G,pos,edgelist=weighted_edges,width=weight*len(pos)*1.0/sum(all_weights))

    #4. Label the nodes
    labels = {}
    for node in unique_nodes:
        labels[node] = node
    nx.draw_networkx_labels(G,pos,labels,font_size=16)

    #Plot the graph
    plt.axis('off')
    plt.title('JIRA collaboration analysis')
    plt.savefig("jira_collaboration_analysis.png") 
    plt.show() 


def run_collaboration_analysis(last_n_days=30):
    "Figure out how people are collaborating on JIRA"
    #1. Get a list of collaborators on each ticket
    raw_collaboration_information = get_collaboration_information(last_n_days)
    #2. Plot a weighted network graph
    plot_collaboration_data(raw_collaboration_information)


#----START OF SCRIPT
if __name__=='__main__':
    print 'Script started'
    run_collaboration_analysis(15)
