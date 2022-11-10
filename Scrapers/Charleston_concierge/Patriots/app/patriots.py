from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

sleep(15)

browser = webdriver.Remote('http://patriots:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
browser.get("http://www.duneswestgolfclub.com/-book-a-tee-time(2)")
# browser.get("https://python.org")
browser.save_screenshot('patriots_screenshot.png')
