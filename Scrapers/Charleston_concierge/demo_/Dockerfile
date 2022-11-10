FROM python:3.7-alpine

# used to send the output to terminal  without buffering
ENV PYTHONUNBUFFERED 1 

# copy desired requirements file  and run pip 
COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt

# create directory on image to  store source code and cd to it. 
RUN mkdir /app
COPY ./app /app
WORKDIR /app
