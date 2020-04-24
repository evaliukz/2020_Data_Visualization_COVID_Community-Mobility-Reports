#!/usr/bin/env python
# coding: utf-8

# In[143]:


##data processing
import pandas as pd
import numpy as np

##data visualization
import plotly.express as px
import matplotlib.pyplot as plt 

##user interaction
import ipywidgets as widgets
from IPython.display import display


# In[144]:


df = pd.read_csv("https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=911a386b6c9c230f",
                dtype={'country_region_code':str,
                                 'country_region':str,
                                 'sub_region_1':str,
                                 'sub_region_2':str,
                                 'retail_and_recreation_percent_change_from_baseline':np.float,
                                 'grocery_and_pharmacy_percent_change_from_baseline':np.float,
                                 'parks_percent_change_from_baseline':np.float,
                                 'transit_stations_percent_change_from_baseline':np.float,
                                 'workplaces_percent_change_from_baseline':np.float,
                                 'residential_percent_change_from_baseline':np.float},
                          parse_dates = ['date']   ## this is good to know
                )
df.head()


# In[202]:


datasets_list = list(df.columns.values)[5:]
dataset_picker = widgets.Dropdown(options=datasets_list, value=datasets_list[0])
dataset_picker


# In[203]:


state_list = df[df['country_region']=='United States']['sub_region_1'].unique().tolist()[1:]
state_picker = widgets.Dropdown(options=state_list, value=state_list[0])
state_picker


# In[212]:


## County-level Data##
def multiple_states_data_select (country, state):
    Criteria=(df ['country_region']==country)&(df['channel']==state_picker.value)
    result= df.loc[Criteria].dropna(subset=['sub_region_2']).fillna(0)
    return result

selected_data = state_data_select ('United States',state_picker.value)
fig = px.line(selected_data, x='date',y=dataset_picker.value,color='sub_region_2')
fig.update_layout(
    height=800,
    title_text= state_picker.value
)
fig.show()


# In[211]:


## Multi-state Data##
states = ['California','New York','Florida','Texas','Illinois']
def multiple_states_data_select (country, states):
    Criteria=(df ['country_region']==country)&(df['sub_region_1'].isin(states))
    result=df.loc[Criteria].dropna(subset=['sub_region_2']).fillna(0)
    result=result.groupby(['sub_region_1','date'])[dataset_picker.value].mean().reset_index()
    return result

selected_states = multiple_states_data_select ('United States',states)
fig = px.line(selected_states, x='date',y=dataset_picker.value,color='sub_region_1')
fig.show()


# In[ ]:





# In[ ]:




