import pandas as pd 
import numpy_financial as npf
from datetime import date, datetime

def get_schedules(property_vars, extra_payment= None):
    '''
Scenario #2 — Dynamic payment based on % of rental cash flow
Start Rent — rent value at the start of the mortgage
Start Cash Flow — after income and expenses the net value you pocket
Rent Increase YoY — expected increase in rent year over year 
                    (standard increase typically 3–5%)
Extra Payment % — percentage of cash flow to contribute towards extra payments 
                (i.e. 10% of $300 cash flow = $30 applied to mortgage principal each month 
                for that year)'''
    
    interest = property_vars['interest']
    years = property_vars['years']
    payments_year = property_vars['payments_year']
    mortgage = property_vars['mortgage']
    start_date =property_vars['start_date']  
    mortgage_type =property_vars['term']
    # print(mortgage_type)
    # scenario 1
#     extra_payment = 0
    # scenario 2
    start_rent = None 
    start_cash_flow = None
    rent_increase_yoy = None
    extra_payment_prct = None
    
    
    # initial values for monthly payment, interest and principal
    initial_pmt = -1 * npf.pmt(interest/12, years*payments_year, mortgage)
    initial_ipmt = -1 * npf.ipmt(interest/payments_year,1, years*payments_year, mortgage)
    initial_ppmt = -1 * npf.ppmt(interest/payments_year, 1,years*payments_year, mortgage)
    
    # create DF
    if mortgage_type == 'jumbo':        
        rng = pd.date_range(start_date, periods=property_vars["payback_years"] * payments_year, freq='MS')
        final_period = property_vars['payback_years'] * 12
    else:
        rng = pd.date_range(start_date, periods=years * payments_year, freq='MS')          
    rng.name = "Payment Date"
    
    # create dataframe 
    full_df = pd.DataFrame(
        index= rng,
        columns=['Org Total Payment','Total Payment','Interest','Principal',
                 'Additional Payment','Org Ending Balance','Ending Balance'], dtype='float')
    full_df.reset_index(inplace=True)
    full_df.index += 1
    full_df.index.name ="Period"

    if (start_rent!= None) and (start_cash_flow != None) and (rent_increase_yoy !=None) and (extra_payment_prct !=None):
        initial_additional_pmt = start_cash_flow * extra_payment_prct
    elif extra_payment != None:
        initial_additional_pmt = extra_payment
    else:
        initial_additional_pmt = 0     
    
    # Create values for the first period
    period = 1
    # for each element in the row set the value
    if mortgage_type == 'int_only': 
        initial_row_dict = {
            'Org Total Payment': initial_ipmt,
            'Total Payment': initial_ipmt + (initial_additional_pmt),
            'Interest': initial_ipmt,
            'Principal': 0.0,
            'Additional Payment': initial_additional_pmt, 
            'Org Ending Balance': mortgage,
            'Ending Balance': mortgage - (initial_additional_pmt)    
            }    
    else:
        initial_row_dict = {
            'Org Total Payment': initial_pmt,
            'Total Payment': initial_pmt + (initial_additional_pmt),
            'Interest': initial_ipmt,
            'Principal': initial_ppmt,
    #         'Rent': start_rent,
    #         'Cash Flow': start_cash_flow,
            'Additional Payment': initial_additional_pmt, 
            'Org Ending Balance': mortgage - initial_ppmt,
            'Ending Balance': mortgage - initial_ppmt - (initial_additional_pmt)    
            }
    columns = list(initial_row_dict.keys())
    period_values = list(initial_row_dict.values())
    full_df.at[period, columns] = period_values
    # round values 
    full_df = full_df.round(2)
    if property_vars['term'] == 'jumbo':
        full_df = full_df[:final_period]
    
    # Add the rest of the rows 
    for period in range(2, len(full_df)+1):
        # get the prior period values 

        previous_total_payments = full_df.loc[period-1,'Total Payment']
        previous_principal = full_df.loc[period-1,'Principal']
        previous_org_ending_balance = full_df.loc[period-1,'Org Ending Balance']
        previous_ending_balance = full_df.loc[period-1,'Ending Balance']
        previous_= full_df.loc[period-1,'Total Payment']
        
        ######
        # Check if Jumbo and add lump due if period met
        ######
        if property_vars['term'] == 'jumbo':            
            if period == final_period:
                extra_payment = previous_ending_balance
                initial_additional_pmt = previous_ending_balance
        
        # get additional payment values
        if (start_rent!= None) and (start_cash_flow != None) and (rent_increase_yoy !=None) and (extra_payment_prct !=None):
            if period % 13 == 0:
                period_rent = previous * (1 + rent_increase_yoy)
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
        
        if mortgage_type == 'int_only': 
            row_dict = {
                'Org Total Payment': initial_ipmt,
                'Total Payment': initial_ipmt + (initial_additional_pmt),
                'Interest': initial_ipmt,
                'Principal': 0.0,
                'Additional Payment': initial_additional_pmt, 
                'Org Ending Balance': mortgage,
                'Ending Balance': mortgage - (initial_additional_pmt)    
                }    
        else:
            row_dict = {
                'Org Total Payment': initial_pmt,
                'Total Payment': initial_pmt + period_additional_pmt,
                'Interest': period_interest,
                'Principal': period_principal,
                'Additional Payment': period_additional_pmt, 
                'Org Ending Balance': org_ending_balance,
                'Ending Balance': ending_balance    
                }

        columns = list(row_dict.keys())
        period_values = list(row_dict.values())
        full_df.loc[period, columns] = period_values
        full_df = full_df.round(2)
    if property_vars['term'] == 'jumbo':
        full_df = full_df[:final_period]

    return full_df