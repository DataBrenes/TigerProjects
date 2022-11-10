FROM python:3.9-slim


# RUN apt-get update && \
#     apt-get install -y locales && \
#     sed -i -e 's/# en_US.utf8 UTF-8/en_US.utf8 UTF-8/' /etc/locale.gen && \
#     dpkg-reconfigure --frontend=noninteractive locales

# Set the locale
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

COPY ./requirements.txt /requirements.txt 
RUN pip3 install -r /requirements.txt

# create directory on image to  store source code and cd to it. 
RUN mkdir /app
COPY ./app /app
WORKDIR /app

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "chart.py", "--server.port=8501", "--server.address=0.0.0.0"]