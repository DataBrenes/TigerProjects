from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

logging.basicConfig(filename='logs/booking.log', level=logging.INFO)

def check_new(df):
    if len(df.index) == 0:
        logging.info('No new booking found.')
    else:
        logging.info('New booking found.')


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
    ## download reservations 
    # export=browser.find_element(by=By.XPATH, value="//input[@value='Export']")
    # export.click()
    # sleep(2)
    
    # get reservations from web
    html = browser.page_source
    table = pd.read_html(html)
    res_df = table[0]
    res_file=gp.get_params('reservations')
    # check if res id exists
    curr = pd.read_csv(res_file['all_res'])
    new_res=res_df[['Res. #','Guest','Check-In','Checkout','Nights']]
    new_res.columns = ['Res_ID','Guest','CheckIn','CheckOut','Nights']
    n_df=cn.checkNewRes(curr,new_res)

    # Check if new
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
    master_df.to_csv(res_file['all_res'],index=False)
    logging.info("Updating Master List")

    logging.info("Closing Browser")
    browser.close()

    stop_time = datetime.now()    
    next_time = stop_time + timedelta(minutes=30)
    logging.info('Done checking for bookings, next check in 30 min ( '+next_time.strftime("%H:%M:%S") +' )')
    logging.info(stop_time.strftime("%m/%d/%Y %H:%M:%S"))

    sleep(1800)