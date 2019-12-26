#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
from datetime import datetime

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', -1)
from pandas.io.json import json_normalize
import json
import ast

get_ipython().run_line_magic('load_ext', 'autotime')

import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)


# In[33]:


commits = pd.read_csv('data/commits.csv', parse_dates=True)


# In[34]:


commits.info()


# ## Data Preprocessing

# In[56]:


commits['date'] =  pd.to_datetime(commits['commit.committer.date'])


# In[57]:


commits['date'] =  pd.to_datetime(commits['date'], utc=True)


# In[58]:


commits['commit_date'] = commits['date'].dt.date


# In[59]:


commits['commit_week'] = commits['date'].dt.week


# In[60]:


commits['commit_hour'] = commits['date'].dt.hour


# In[61]:


commits['commit_month'] = commits['date'].dt.month


# In[62]:


commits['commit_year'] = commits['date'].dt.year


# In[63]:


# drop unnecessary columns
commits = commits[['sha', 'author.login', 'commit_date', 'commit_hour', 'commit_month', 'commit_year']]


# In[79]:


commits.head()


# ## Data Analysis

# In[91]:


## number of contributors
commits['author.login'].unique().size


# In[92]:


commits_by_hour = commits.groupby('commit_hour')[['sha']].count()
commits_by_hour = commits_by_hour.rename(columns = {'sha': 'commit_count'})


# In[93]:


fig = go.Figure([go.Bar(
    x=commits_by_hour.index, 
    y=commits_by_hour.commit_count, 
    text=commits_by_hour.commit_count, 
    textposition='auto')])
fig.update_layout(
    title = 'Commits by Hour', 
    xaxis_title = 'Hour', 
    yaxis_title = 'Commits Count', 
    xaxis_tickmode = 'linear')
fig.show()


# In[94]:


commits_by_day = commits.groupby('commit_date')[['sha']].count()
commits_by_day = commits_by_day.rename(columns = {'sha': 'commit_count'})


# In[95]:


fig = go.Figure([go.Scatter(
    x=commits_by_day.index, 
    y=commits_by_day.commit_count, 
    text=commits_by_day.commit_count, 
    fill='tozeroy')])
fig.update_layout(
    title = 'Commits by Date', 
    xaxis_title = 'Date', 
    yaxis_title = 'Commits Count')
fig.show()


# In[96]:


commits_by_author = commits.groupby('author.login')[['sha']].count()
commits_by_author = commits_by_author.rename(columns = {'sha': 'commit_count'})
commits_by_author = commits_by_author.sort_values(by='commit_count', ascending=False)
top_authors = commits_by_author.head(30)


# In[97]:


fig = go.Figure([go.Bar(
    x=top_authors.index, 
    y=top_authors.commit_count)])
fig.update_layout(
    title = 'Top Committers', 
    xaxis_title = 'Author', 
    yaxis_title = 'Commits Count', 
    xaxis_tickmode = 'linear',
    xaxis_tickangle=-40)
fig.show()


# ## Open Pull Requests

# In[98]:


pulls = pd.read_csv('data/pulls.csv', parse_dates=True)


# In[99]:


pulls.info()


# In[100]:


pulls['date'] = pd.to_datetime(pulls['created_at'])
pulls['date'] = pd.to_datetime(pulls['date'], utc=True)
pulls['pull_date'] = pulls['date'].dt.date


# In[101]:


pulls_by_date = pulls.groupby('pull_date')[['id']].count()
pulls_by_date = pulls_by_date.rename(columns = {'id': 'commit_count'})


# In[104]:


fig = go.Figure([go.Scatter(
    x=pulls_by_date.index, 
    y=pulls_by_date.commit_count, 
    text=pulls_by_date.commit_count)])
fig.update_layout(
    title = 'Open Pull Requests by Date', 
    xaxis_title = 'Date', 
    yaxis_title = 'Pulls Count')
fig.show()


# ### Pull Request Labels

# **NOTES**:  
# - ast.literal_eval converts string to list.
# - The following two lines convert a Pandas column that contains list of dictionaries into a Pandas Dataframe where each dictionary corresponds to a dataframe row.

# In[105]:


labels_list = [ast.literal_eval(i) for i in pulls['labels'].tolist() if i != '[]']


# In[106]:


labels = [j for i in labels_list for j in i]


# In[108]:


labels_df = pd.DataFrame(labels)


# In[114]:


labels_by_name = labels_df.groupby('name')[['id']].count()
labels_by_name = labels_by_name.rename(columns = {'id': 'label_count'})
labels_by_name = labels_by_name.sort_values(by=['label_count'], ascending=False)


# In[115]:


fig = go.Figure([go.Bar(
    x=labels_by_name.index, 
    y=labels_by_name.label_count)])
fig.update_layout(
    title = 'Pull Requests by Label', 
    xaxis_title = 'Labels', 
    yaxis_title = 'PR Count', 
    xaxis_tickmode = 'linear',
    xaxis_tickangle=-40)
fig.show()

