from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


def available(driver,day,park):
    alert = None
    park_list = []

    CheckAll = """ return document
    .querySelector("#container > app-availability-calendar > awakening-calendar").shadowRoot
    .querySelectorAll("#calendarContainer > wdat-calendar > wdat-date")"""

    all_dates= driver.execute_script(CheckAll)

    for date in all_dates:
        new = date.get_attribute("aria-label")
        if new == 'Sunday, May 29, 2022':
            sun = date
            # print("found the date "+new)
        if new == 'Monday, May 30, 2022':
            mon = date
            # print("found the date "+new)   
        if new == 'Sunday, May 22, 2022':
            test = date
            # print("found the date "+new)  

    if day.lower() == 'sunday':
        parkday = sun
    if day.lower() == 'monday':
        parkday = mon
    if day.lower() == 'test':
        parkday = test

    if park.lower() == 'magic':
        condition = 'Magic Kingdom'
    if park.lower() == 'holly':
        condition = 'Hollywood Studios'
    if park.lower() == 'animal':
        condition = 'Animal Kingdom'
    if park.lower() == 'epcot':
        condition = 'EPCOT'
    
    # CheckDay = """ return document """
    # .querySelector("#container > app-availability-calendar > awakening-calendar").shadowRoot
    # .querySelector("#calendarContainer > wdat-calendar > wdat-date:nth-child("""+str(num)+"""") 
    # date_run= driver.execute_script(CheckDay)


    date = parkday.get_attribute("aria-label")
    park_list.append(date)
#     print(date)

    parkday.click()   
    sleep(3)
    
    for i in range(1,5):     
        sub = 'does not have'
        query= """return document
        .querySelector("#container > app-availability-calendar > awakening-availability-information").shadowRoot
        .querySelector("#parkAvailabilityContainer > div:nth-child("""+str(i)+""") > dprd-icon")"""
        status = driver.execute_script(query).get_attribute("aria-label")
        if sub not in status:
            park_list.append(status)
#             print(status)
            
    for a in park_list:
        if condition in a:
            alert ="On "+park_list[0]+' '+a
    message = alert
    return message   
