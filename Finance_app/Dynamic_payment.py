import os
import json
import pandas as pd

def add_extra_pay(df,date, extra_payment, interest, payments_year, morgterm, lump = None):
    initial_pmt=df.loc[1,'Org Total Payment']
    start_date = df[df['Payment Date'] == date].index[0]
    period_additional_pmt = extra_payment
    
    for period in range(1, len(df)+1):

        if period == start_date:
            if lump != None:
                if period == lump[0]:
                    print("lump apply date: "+ str(lump[0]))
                    period_additional_pmt = lump[1]
                else:
                    period_additional_pmt = extra_payment
    #         print("Start making additional payments "+ str(df.loc[period,'Payment Date']))
            for p in range(period, len(df)+1):
                
                
                # get the prior period values 
                previous_total_payments = df.loc[p-1,'Total Payment']
                previous_principal = df.loc[period-1,'Principal']
                previous_org_ending_balance = df.loc[p-1,'Org Ending Balance']
                previous_ending_balance = df.loc[p-1,'Ending Balance']
                previous_= df.loc[p-1,'Total Payment']

                # Calculate remainder values to get the end of loan bal
                period_interest = previous_org_ending_balance * interest / payments_year
                if morgterm == 'int_only':
                    period_principal = 0.0
                else:
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
                'Additional Payment': period_additional_pmt, 
                'Org Ending Balance': org_ending_balance,
                'Ending Balance': ending_balance
                }

                columns = list(row_dict.keys())
                period_values = list(row_dict.values())
                df.loc[p, columns] = period_values
                df = df.round(2)
    end_date = df[df['Ending Balance'] == 0.00].index[0]
    payoff_date=df.loc[end_date,'Payment Date']
    avail_cashflow=df.loc[end_date,'Total Payment']
    final_df = df[:end_date]
    return payoff_date, avail_cashflow,final_df