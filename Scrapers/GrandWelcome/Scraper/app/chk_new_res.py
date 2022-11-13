import pandas as pd

def checkNewRes(df1,df2):
    ''' Takes the saved list df1 and compares it to recent pullsed list df2. 
    New reservations get added to list and saved as csv. 
    Returns dataframe of new reservations'''
    
    final_list=[]
    master_df=df1.copy()
    final_df= pd.DataFrame(columns=master_df.columns)
    
    mast_list=df1['Res_ID'].to_list()
    new_list=df2['Res_ID'].to_list()
    # master_df=curr.copy()

    for n in new_list:
        if n in mast_list:
            pass
            # print("duplicate")
        else:
            final_list.append(n)

    for f in final_list:
        nrow=df2.loc[df2['Res_ID'] == f]
        master_df = pd.concat([nrow, master_df])
        final_df = pd.concat([nrow, final_df])
        
    master_df.to_csv('reservations/All_reservations.csv',index=False)
    
    return final_df
    
