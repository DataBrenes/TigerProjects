# Base requirements
As we continue to modulize and simplify the scraper process these are some of the common requirements. 
## Selenium chrome docker image 
***This DOES NOT run on a pi (arm64)***
```
docker run -d -p 4444:4444 -p 7900:7900 --name selenium4 --shm-size="2g" selenium/standalone-chrome:4.4.0-20220831
```
## Selenium pi Image 
There is an experimental multi platform image located [here](https://github.com/seleniumhq-community/docker-seleniarm)
CHROME  
***At time of writing used this one `docker pull seleniarm/standalone-chromium:107.0`***
```
docker run --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size 2g seleniarm/standalone-chromium:latest
```
FIREFOX  
```
docker run --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size 2g seleniarm/standalone-firefox:latest
```

This is the first attempt at dockerizing some of the scraper apps. Step one is to get the selenium 4 docker image. The ![quick start](https://github.com/SeleniumHQ/docker-selenium#quick-start)  also has docker compose examples to show how to run selenium 4 grid.  

### Download Chrome image 
```
docker run -d -p 4444:4444 -p 7900:7900 --name selenium4 --shm-size="2g" selenium/standalone-chrome:4.4.0-20220831
```

Port 7900 is the no vnc port number for seeing what is happening in the docker container. This can be mapped to whatever. `localhost:7900`  
Password is `secret`  

### Testing remote driver with jupyter notebook 

If you open the the novnc port at 7900 and run the following block, you should be able to see the chrome browser open up and see it open the website
```

from selenium import webdriver 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
caps = DesiredCapabilities.CHROME
browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=caps)
browser.get("http://www.duneswestgolfclub.com/-book-a-tee-time(2)")
```


### DockerFile Example 
```
FROM python:3.7-alpine

# used to send the output to terminal  without buffering
ENV PYTHONUNBUFFERED 1 

# copy desired requirements file  and run pip 
COPY ./requirements.txt / requirements.txt 
RUN pip install -r requirements.txt

# create directory on image to  store source code and cd to it. 
RUN mkdir /app
COPY ./app /app
WORKDIR /app
```
### Docker Compose 
```
version:"3"

services:
  patriots_point: 
    image: selenium/standalone-chrome:4.4.0-20220831
    ports: 
    - 4444:4444
    - 7900:7900

    restart: always

  app:
    build:
      context: .
    volumes:
     - ./app:/app
    command: sh -c "python3 patriots.py"
    depends_on:
     - patriots_point 
```
#### Create image 

run the command `docker-compose build ` ***In Powershell!!*** wsl bombs because it sends case sensitive command to docker. 