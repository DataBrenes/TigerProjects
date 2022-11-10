import Mortgage_schedules as ms
import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

# Load the data
l = open('loans.json')
loans = json.load(l)

schedules = {}
for m in loans:
    schedules[m]= ms.get_schedules(loans[m])

# plot the data
fig = go.Figure()
for i in schedules:
    fig = fig.add_trace(go.Scatter(x = schedules[i]["Payment Date"],
                                   y = schedules[i]["Ending Balance"], 
                                   name = i))
fig.update_layout(
  title='Mortgage Amoritization', 
  xaxis_title='Year', 
  yaxis_title='Mortgage Balance', 
  plot_bgcolor='light blue',
  legend=dict(
    title_text="Home",
    # yanchor="top",
    y=1.02,
    # xanchor="right",
    x=1.01))


st.plotly_chart(fig, use_container_width=True)