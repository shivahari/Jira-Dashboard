# Jira Dashboard


## Why?

JIRA is great for issue level tracking. However, it sucks at:

a) showing timelines well (most small teams are prone to 'bursty' behavior)

b) showing the big picture (do you know what each of your previous sprints focused on?)

c) how individuals are collaborating (we all have that one silent person in our teams!)

----

## What?

This project is going to try and wrestle some useful data out of JIRA and present timelines and (hopefully) the big picture.

## Background:

This work was done in a team of two as part of the Qxf2 Hackathon on 12-Oct-2017. The work here is from a Hackathon not representative of my/our coding standards.

----

## Setup:

1. Clone this repo

2. Create a credentials.py in the root directory of this project and provide the following:

### USERNAME='Your JIRA username'

### PASSWORD='Your JIRA password'

### JIRA_URL='https://your_JIRA_URL'

### PROJECT='Your Project name'

3. (Until the web app is developed) Run the different .py scripts and once they have run, open the corresponding html files in your browser

a) get_issues_in_qa.py > in_qa_status.html

b) analyze_description_habits.py > description_average_words.html

c) qa_queue_arrival_timeline.py > qa-arrival.html

d) state_time_breakdown.py > state-time-breakdown.html

e) analyze_connections.py > analyze-collaboration.html

f) 