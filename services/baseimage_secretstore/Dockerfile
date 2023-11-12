# Use Python 3.11.4
FROM python:3.11.4

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY ./requirements.txt .
# Install any needed packages specified in requirements.txt
# install dependencies
RUN apt-get update && apt-get install -y netcat-traditional
RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip uninstall werkzeug -y
RUN pip install --trusted-host pypi.python.org werkzeug==2.3.7