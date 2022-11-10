import pandas as pd 
import numpy_financial as npf
from datetime import date, datetime
import plotly.express as px
import streamlit as st

# variables Turnstone 
Turnstone = {
"interest" :0.03125,
"years":30, 
"payments_year":12,
"mortgage":436000,
"start_date":(date(2020, 12, 1))
}

# variables Turnstone Heloc  
Heloc = {
"interest" :0.075,
"years":30, 
"payments_year":12,
"mortgage":98039.88,
"start_date":(date(2022, 3, 9))
}

# variables Brier Rose  
LakeSide = {
"interest" :0.03375,
"years":30, 
"payments_year":12,
"mortgage":277520,
"start_date":(date(2022, 3, 1))
}

# variables Brier Rose  
BrierRose = {
"interest" :0.03375,
"years":30, 
"payments_year":12,
"mortgage":277520,
"start_date":(date(2021, 3, 1)),
"Current_payment":1767.56,
"HOA_club":161.25,
"HOA_resort":204.00
}

def get_mortgage_amoritization(property_vars, extra_payment= None):
    interest = property_vars['interest']
    years = property_vars['years']
    payments_year = property_vars['payments_year']
    mortgage = property_vars['mortgage']
    start_date =property_vars['start_date']    
    start_rent= None
    start_cash_flow=None
    rent_increase_yoy=None
    extra_payment_prct=None
    
    # initial valuies for monthly payment, interest and principal
    initial_pmt = -1 * npf.pmt(interest/12, years*payments_year, mortgage)
    initial_ipmt = -1 * npf.ipmt(interest/payments_year,1, years*payments_year, mortgage)
    initial_ppmt = -1 * npf.ppmt(interest/payments_year, 1,years*payments_year, mortgage)
    
    # create DF 
    rng = pd.date_range(start_date, periods=years * payments_year, freq='MS')
    rng.name = "Payment Date"
    # create dataframe 
    df = pd.DataFrame(
        index= rng,
        columns=['Org Total Payment','Total Payment','Interest','Principal','Rent','Cash Flow',
                 'Additional Payment','Org Ending Balance','Ending Balance'], dtype='float')
    df.reset_index(inplace=True)
    df.index += 1
    df.index.name ="Period"
    
#     print("extra payment =" + str(extra_payment))
#     print(type(extra_payment))
#     print("start rent =" + str(start_rent))
#     print(type(start_rent))
    # test if additional cash flow from rent is passed as an arg 
    if (start_rent != None ) and (start_cash_flow != None) and (rent_increase_yoy != None) and (extra_payment_prct != None):
        initial_additional_pmt = start_cash_flow * extra_payment_prct
    elif extra_payment != None:
        initial_additional_pmt = extra_payment
    else:
        initial_additional_pmt = 0
        
    # Create values for the first period
    period = 1
    # for each element in the row set the value
    initial_row_dict = {
        'Org Total Payment': initial_pmt,
        'Total Payment': initial_pmt + (initial_additional_pmt),
        'Interest': initial_ipmt,
        'Principal': initial_ppmt,
        'Rent': start_rent,
        'Cash Flow': start_cash_flow,
        'Additional Payment': initial_additional_pmt, 
        'Org Ending Balance': mortgage - initial_ppmt,
        'Ending Balance': mortgage - initial_ppmt - (initial_additional_pmt)    
    }
    columns = list(initial_row_dict.keys())
    period_values = list(initial_row_dict.values())
    df.at[period, columns] = period_values
    # round values 
    df = df.round(2)
    
    # Add the rest of the rows 
    for period in range(2, len(df)+1):
        # get the prior period values 
    #     print(period)
        previous_total_payments = df.loc[period-1,'Total Payment']
        previous_principal = df.loc[period-1,'Principal']
        previous_rent = df.loc[period-1,'Rent']
        previous_cf = df.loc[period-1,'Cash Flow']
        previous_org_ending_balance = df.loc[period-1,'Org Ending Balance']
        previous_ending_balance = df.loc[period-1,'Ending Balance']
        previous_= df.loc[period-1,'Total Payment']

        # set additional payment values 
        # 1 Dynamic additional payment
        # 2 Fixed additional payment 
        # 3 No additional payment 
        if (start_rent != None ) and (start_cash_flow != None) and (rent_increase_yoy != None) and (extra_payment_prct != None):
            if period % 13 == 0:
                period_rent = previous_rent * (1 + rent_increase_yoy)
            else:
                period_rent = previous_rent

            period_cash_flow = previous_cf + (period_rent - previous_rent)
            period_additional_pmt = period_cash_flow * extra_payment_prct
        elif extra_payment != None:
            period_additional_pmt = initial_additional_pmt
            period_rent = 0 
            period_cash_flow = 0
            extra_payment_prct = 0 
        else:
            period_additional_pmt = 0 
            period_rent = 0 
            period_cash_flow = 0
            extra_payment_prct = 0

        # Calculate remainder values to get the end of loan bal
        period_interest = previous_org_ending_balance * interest / payments_year
        period_principal = initial_pmt - period_interest
        org_ending_balance = previous_org_ending_balance - period_principal
        ending_balance = previous_ending_balance - period_principal - period_additional_pmt
        org_ending_balance = 0 if org_ending_balance <= 0 else org_ending_balance
        ending_balance = 0 if ending_balance <= 0 else ending_balance

        row_dict ={
        'Org Total Payment': initial_pmt,
        'Total Payment': initial_pmt + period_additional_pmt,
        'Interest': period_interest,
        'Principal': period_principal,
        'Rent': period_rent,
        'Cash Flow': period_cash_flow,
        'Additional Payment': period_additional_pmt, 
        'Org Ending Balance': org_ending_balance,
        'Ending Balance': ending_balance
        }
        columns = list(row_dict.keys())
        period_values = list(row_dict.values())
        df.loc[period, columns] = period_values
        df = df.round(2)
    return df
## Get initial Schedules

turn_df=get_mortgage_amoritization(Turnstone)
mike_month=1185.25 * 2
br_df=get_mortgage_amoritization(BrierRose,mike_month)

# # initial valuies for monthly payment, interest and principal
# initial_pmt = -1 * npf.pmt(interest/12, years*payments_year, mortgage)
# initial_ipmt = -1 * npf.ipmt(interest/payments_year,1, years*payments_year, mortgage)
# initial_ppmt = -1 * npf.ppmt(interest/payments_year, 1,years*payments_year, mortgage)

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (round(num), ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

#################
# Visualization #
#################
df_plot = pd.melt(turn_df, id_vars=['Payment Date'], value_vars=['Org Ending Balance', 'Ending Balance'])
df_plot

# get last payment for early payoff
early_payment_date = df_plot.loc[(df_plot['variable'] == 'Ending Balance') & (df_plot['value'] == 0)]['Payment Date'].min().strftime('%Y-%m-%d')
# get max payment date
max_payment_date = df_plot['Payment Date'].max().strftime('%Y-%m-%d')
# get savings in interest
additional_interest = turn_df.loc[turn_df['Payment Date'] > early_payment_date]['Interest'].sum()

print('Early payment date:', early_payment_date)
print('End payment date:', max_payment_date)
print('Additonal interest:', additional_interest)

# create plotly chart
fig = px.line(df_plot, x='Payment Date', y='value', color='variable')
fig.add_vline(x=early_payment_date, line_dash="dot", line_color="black")
fig.add_vrect(
  x0=early_payment_date, 
  x1=max_payment_date, 
  fillcolor="red", 
  opacity=0.25, 
  annotation_position="top left",
  annotation_text="+${0} interest savings".format(human_format(additional_interest))
)
fig.update_layout(
  title='Mortgage Amoritization', 
  xaxis_title='Year', 
  yaxis_title='Mortgage Balance', 
  plot_bgcolor='white',
  legend=dict(
    title_text="Balance Type",
    yanchor="bottom",
    y=0.02,
    xanchor="left",
    x=0.01)
)
# st.fig.show()

st.plotly_chart(fig, use_container_width=True)