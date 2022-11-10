# added style changes  

#TODO
#1: Remove gridlines and background color  - Done 
#2: Keep consistent colors across graphs - Not Working 
#3: Use spikelines to compare data points - Done
#4: Remove floating menu, disable zoom and adjust click behavior - Done


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

# Generate graph using Figure Constructor
layout = go.Layout(
    plot_bgcolor="#5C5D67",
    hovermode="x",
    hoverdistance=100, # Distance to show hover label of data point
    spikedistance=1000, # Distance to show spike
    title='Mortgage Amoritization',
    xaxis_title='Year',
    yaxis_title='Mortgage Balance'
)

COLORS_MAPPER = {
    "Turnstone": "#074F57",
    "Heloc": "#5AAA95",
    "LakeSide": "#897C80",
    "BrierRose": "#CAB6CD"
}
# plot the data
fig = go.Figure()
for i in schedules:
    fig = fig.add_trace(go.Scatter(x = schedules[i]["Payment Date"],
                                   y = schedules[i]["Ending Balance"], 
                                   name = i))
    fig.update_xaxes(dict(linecolor=COLORS_MAPPER[i]))

fig.update_layout(layout)
# remove grid lines add spike line and format
fig.update_xaxes(
  showgrid=False,
  showspikes=True,
  spikethickness=2,
  spikedash="dot",
  spikecolor="#999999",
  spikemode="across"                 
                 )
fig.update_yaxes(showgrid=False)
# Remove floating menu
config={"displayModeBar": False, "showTips": False}

st.plotly_chart(fig, use_container_width=True,config=config)