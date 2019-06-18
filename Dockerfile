# Use an official Python runtime as a parent image
FROM python:latest

LABEL maintainer="ziggerzz@gmail.com"

# Set working directory
WORKDIR /adam_qas

# First copy and install the requirements so further cache can be used
COPY ./requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=3000 --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /adam_qas