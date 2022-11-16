from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import json
import get_params as gp
import chk_new_res as cn
import build_payload as bp
import send2cal as cal
import logging
import re
from dateutil.parser import parse
from datetime import date, timedelta
logging.basicConfig(filename='logs/booking.log', level=logging.INFO)

def check_new(df):
    if len(df.index) == 0:
        logging.info('No new booking found.')
    else:
        logging.info('New booking found.')

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
        month = t.strftime("%b")+'-'+t.strftime("%Y")
        if month in BookedDaysPerMonth:
            BookedDaysPerMonth[month] += 1
        else:
            BookedDaysPerMonth[month] = 1
    Dates_list=[]
    for k,v in BookedDaysPerMonth.items():
        Dates_list.append('{}-{}'.format(k,v))
    return Dates_list


sleep(15)

while True:
    start_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    logging.info('Starting new booking check')
    logging.info(start_time)

    cred = gp.get_params('login')
    browser = webdriver.Remote('http://bookings:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    browser.get(str(cred['url']))

    # Login 
    username=browser.find_element(by=By.XPATH, value="//input[@placeholder='Email']")
    password=browser.find_element(by=By.XPATH, value="//input[@placeholder='Password']")
    login=browser.find_element(by=By.XPATH, value="//button[@type='submit']")
    username.send_keys(str(cred['user']))
    password.send_keys(str(cred['password']))
    login.submit()

    sleep(5)

    ## click reservations tab
    restab=browser.find_element(by=By.XPATH, value="//span[normalize-space()='Reservations']")
    restab.click()
    sleep(5)

    ## Need to make sure that 100 is showing instead of 10
    select = Select(browser.find_element(by=By.XPATH, value="//*[@id='table_length']/label/select"))
    # select by value 
    select.select_by_value('100')
    sleep(5)
    # Get table 
    html = browser.page_source
    table = pd.read_html(html)
    res_raw_df = table[0]
    res_df=res_raw_df[['Res. #', 'Status', 'Unit', 'Guest', 'Booked Date', 'Check-In','Checkout', 'Nights', 'Income']]
    res_df.columns = ['Res_ID', 'Status', 'Unit', 'Guest', 'Booked Date', 'Check-In','Checkout', 'Nights', 'Income']



# Cutting out loop for now as it keeps getting stuck for some reason
#    # check if another page 
#    table=browser.find_element(by=By.XPATH, value='//*[@id="table_paginate"]/ul')
#    items = table.text.split()
#    items.remove('Previous')
#    items.remove('Next')

    ## download reservations 
    # export=browser.find_element(by=By.XPATH, value="//input[@value='Export']")
    # export.click()
    # sleep(2)
# multiple pages 

# Try and find a way to check the "showing  blank  to blank of blank entries" to trigger a next
#    webtables = []
#    for page in items:
        # set to 100 
#        select = Select(browser.find_element(by=By.XPATH, value="//*[@id='table_length']/label/select"))
        # select by value 
#        select.select_by_value('100')
        # get reservations from web
#        html = browser.page_source
#        table = pd.read_html(html)
#        res_raw_df = table[0]
#        webtables.append(res_raw_df)
        # click next page 
#        nxt=browser.find_element(by=By.XPATH, value='//*[@id="table_next"]/a')
#        nxt.click()  
    
#    combined=pd.concat(webtables)
#    res_df=combined[['Res. #', 'Status', 'Unit', 'Guest', 'Booked Date', 'Check-In','Checkout', 'Nights', 'Income']]
#    res_df.columns = ['Res_ID', 'Status', 'Unit', 'Guest', 'Booked Date', 'Check-In','Checkout', 'Nights', 'Income']

    res_file=gp.get_params('reservations')
    # check if res id exists
    curr = pd.read_csv(res_file['all_res'])
    new_res=res_df[['Res_ID','Guest','Check-In','Checkout','Nights']]
    n_df=cn.checkNewRes(curr,new_res)

    # Check if new save file
    check_new(n_df)

    # Send new to calendar
    logging.info("Updating Calendar")
    result = n_df.to_json(orient="records")
    n_pl=json.loads(result)
    for rec in n_pl:
        cal.Send2Cal(bp.build_pl(rec))

    # save updated file with new booking
    update =[n_df,curr]
    master_df = pd.concat(update)
    master_df.reset_index(drop=True,inplace=True)
    master_df["CheckIn"] = pd.to_datetime(master_df["CheckIn"]).dt.strftime('%b/%d/%Y')
    master_df["CheckOut"] = pd.to_datetime(master_df["CheckOut"]).dt.strftime('%b/%d/%Y')
    master_df.to_csv(res_file['all_res'],index=False)
    logging.info("Updating Master List")

    
    ## merge with old data 
    logging.info("Creating Summary Table")
    # format dates to match for merging
    res_df=res_df.copy()
    res_df["Booked Date"] = pd.to_datetime(res_df["Booked Date"]).dt.strftime('%b/%d/%Y')
    res_df["Check-In"] = pd.to_datetime(res_df["Check-In"]).dt.strftime('%b/%d/%Y')
    res_df["Checkout"] = pd.to_datetime(res_df["Checkout"]).dt.strftime('%b/%d/%Y')
    
    rpts=gp.get_params('reports')
    old=pd.read_csv(rpts['old'])
    frames = [res_df,old]
    summ=pd.concat(frames).reset_index(drop=True)
    summ.to_csv(rpts['all_res_full'],index=False)

    # create a summary table
    summ1=summ[['Res_ID','Check-In','Checkout', 'Nights', 'Income']]
    nightly_rate = []
    for i,b in summ1.iterrows():
        Res_ID = b['Res_ID']
        Arrival = parse(b['Check-In']).date()
        Departure = parse(b['Checkout']).date()
        Income_raw = b['Income']
        Income= float(re.sub(r'[^\d.]', '', Income_raw))
        times = [Arrival + timedelta(days=x) for x in range((Departure-Arrival).days + 1)]
        for t in times:
            nightly = Income / len(times)
            night_form = '{0:.2f}'.format(nightly)
            t_stmp=pd.Timestamp(t)
            nightly_rate.append([Res_ID,t_stmp,float(night_form)])
    breakdown = pd.DataFrame(nightly_rate, columns = ['Res_ID','Date', 'Per Night'])
    breakdown['Month-Year']=breakdown['Date'].dt.strftime('%m/%Y')
    breakdown.drop_duplicates(keep='first', inplace=False).reset_index(drop=True)
    rpts=gp.get_params('reports')
    breakdown.to_csv(rpts['breakdown'],index=False)



    # get updated 
    res_file=gp.get_params('reservations')
    updated = pd.read_csv(res_file['all_res'])
    last_book=updated.loc[0]

    logging.info("Closing Browser")
    browser.close()

    stop_time = datetime.now()    
    next_time = stop_time + timedelta(minutes=30)
    logging.info('Done checking for bookings, next check in 30 min ( '+next_time.strftime("%H:%M:%S") +' )')
    logging.info(stop_time.strftime("%m/%d/%Y %H:%M:%S"))

    sleep(1800)
