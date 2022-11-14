import pandas as pd
import get_params as gp
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import locale 
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
# use This dashboard as a reference
# https://data-science-at-swast-handover-poc-handover-yfa2kz.streamlit.app/
# https://github.com/data-science-at-swast/handover_poc/blob/main/handover.py
## https://altair-viz.github.io/gallery/diverging_stacked_bar_chart.html

#########################
#  KPI 's and Variables #
#########################
def CountDaysMonth(Arrival,Departure):    
    from datetime import date, timedelta
    from dateutil.parser import parse
    from datetime import datetime
    BookedDaysPerMonth = {}
    d1 = parse(Arrival).date()
    d2 = parse(Departure).date()
    # this will give you a list containing all of the dates
    times = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)]
    # Creates a dictionary and increments if it exists 
    for t in times:
        month = t.strftime("%b")+'_'+t.strftime("%Y")
        if month in BookedDaysPerMonth:
            BookedDaysPerMonth[month] += 1
        else:
            BookedDaysPerMonth[month] = 1
    Dates_list=[]
    for k,v in BookedDaysPerMonth.items():
        Dates_list.append('{}-{}'.format(k,v))
    return Dates_list

def get_last_booked(res_full_df):
    from dateutil.parser import parse
    from datetime import datetime 
    today = parse(datetime.now().strftime("%m/%d/%Y")).date()
    book_raw = res_full_df['Booked Date']
    d_list = []
    for date in book_raw:
        d_list.append(parse(date).date())
        
    cloz_dict = { 
      abs(today - date) : date 
      for date in d_list}
    last_booked = cloz_dict[min(cloz_dict.keys())]
    booking=res_full_df.loc[res_full_df['Booked Date'] == last_booked.strftime("%b/%d/%Y")]
    convert=booking.tail(1)
    final=convert.to_dict(orient='records')
    return final

# Import breakdown
rpts=gp.get_params('reports')
costs = gp.get_params('expenses')
breakdown = pd.read_csv(rpts['breakdown'])
# remove duplicates
breakdown = breakdown.drop_duplicates()
breakdown['Date'] =  pd.to_datetime(breakdown['Date'], format='%Y/%m/%d')
# import bookings

rpts=gp.get_params('reservations')
res_full_df=pd.read_csv(rpts['all_res_full'])
get_last=get_last_booked(res_full_df)
#get_last=get_last.to_dict(orient='records')

Mrt_HOA=float(costs['mortgage'])+float(costs['club'])+float(costs['resort'])
op_cost=float(costs['avg_operating'])
# add columns for threshold line
breakdown['MortgageHoa'] = Mrt_HOA
breakdown['opCost'] = op_cost
breakdown['Total'] = Mrt_HOA + op_cost
breakdown=breakdown.sort_values('Date')

# create current month / year filters
current_month_yr = datetime.now().strftime('%m/%Y')
curr_m_name = datetime.now().strftime('%B')
curr_month = datetime.now().strftime('%m')
curr_month_filter = breakdown['Month-Year'] == current_month_yr
curr_year_filter = breakdown['Date'].dt.strftime('%Y') == '2022'
curr_m_df = breakdown[curr_month_filter]
curr_yr_df = breakdown[curr_year_filter]

##########################
# create aggregates
##########################

## Current Monthly Income 
curr_value = sum(curr_m_df['Per Night'])
curr_delta = sum(curr_m_df['Per Night'])-Mrt_HOA-op_cost
## Year to date 
ytd_value = round(sum(curr_yr_df['Per Night']),2)
ytd_delta = round(ytd_value-(int(curr_month))*(Mrt_HOA + op_cost),2)
# All time
total_mrg_mth = len(CountDaysMonth('03/01/2021',datetime.now().strftime('%m/%d/%Y')))
at_value = round(sum(breakdown['Per Night']),2)
at_delta = round(at_value-(total_mrg_mth*(Mrt_HOA + op_cost)),2)
# Last booked payload

l_booked = {
    "value" : get_last[0]['Guest']+' '+str(get_last[0]['Res_ID']),
    "delta" : get_last[0]['Check-In']+'--'+get_last[0]['Checkout']+' |  '+str(get_last[0]['Nights'])+'@ '+get_last[0]['Income']
}
#########################
#        Build chart      #
###########################

# this is the browser tab  and length 
st.set_page_config(page_title='StoryLake Profit/Loss',  layout='wide', page_icon=':anbulance:')

g1, g2, g3 = st.columns((1,1,1))

t1, t2 = st.columns((0.07,1)) 

t1.image('images/StoryLake.png', width = 80)
t2.title("StoryLake Monthly Profit / Loss")


# indicators
m1, m2, m3, m4, m5 = st.columns((1,1,1,1,1))
m1.write('')
m2.metric(label ='Current Income for '+curr_m_name ,value = locale.currency(curr_value, grouping=True), delta = locale.currency(curr_delta, grouping=True) , delta_color = 'normal')
m3.metric(label ='Income Year to Date',value = locale.currency(ytd_value, grouping=True), delta =locale.currency(ytd_delta, grouping=True), delta_color = 'normal')
m4.metric(label = 'Income All Time',value = locale.currency(at_value, grouping=True), delta = locale.currency(at_delta, grouping=True) , delta_color = 'normal')
m5.metric(label = 'Last Booked',value = l_booked['value'] , delta = l_booked['delta'] , delta_color = 'off')
m1.write('')

date_col = st.selectbox('This is the filter box', breakdown, help = 'Filter report to show only one hospital') # need to change this to be year. 

fig = px.histogram(breakdown, x = 'Month-Year', y='Per Night', template = 'seaborn')
## add lines
fig.add_scatter(x=breakdown['Month-Year'], y=breakdown['MortgageHoa'] , mode='lines', line=dict(color="pink"), name='Mortgage + HOA')
fig.add_scatter(x=breakdown['Month-Year'], y=breakdown['Total'] , mode='lines', line=dict(color="green"), name='Bills')
fig.update_traces(marker_color='#7A9E9F')

fig.update_layout(title_text="Monthly Profit/Loss",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)

st.plotly_chart(fig, use_container_width=True)
# Reservations chart 

cw1, cw2 = st.columns((2.5, 1.7))

fig2 = go.Figure(
        data = [go.Table (columnorder = [0,1,2,3,4,5,6,7,8,9,10,11,12], columnwidth = [18,12],
            header = dict(
                values = list(updated.columns),
                font=dict(size=11, color = 'white'),
                fill_color = '#264653',
                # line_color = 'rgba(255,255,255,0.2)',
                align = ['left','center'],
                #text wrapping
                height=20
                )
            , cells = dict(
                values = [updated[K].tolist() for K in updated.columns], 
                font=dict(size=10),
                align = ['left','center'],
                fill_color='black',
                # fill_color = colourcode,
                # line_color = 'rgba(255,255,255,0.2)',
                height=20))])
     
fig2.update_layout(title_text="Reservations",title_font_color = '#264653',title_x=0,margin= dict(l=0,r=10,b=10,t=30), height=600)                                                               

cw1.plotly_chart(fig2, use_container_width=True)  
  

