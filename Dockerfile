# Use an official Python runtime as a parent image
FROM python:3.6-stretch

MAINTAINER  Shirish Kadam <shirishkadam35@gmail.com>

# Set the working directory to /app
WORKDIR /adam_qas

# Copy the current directory contents into the container at /app
COPY . /adam_qas

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=3000 --trusted-host pypi.python.org -r requirements.txt

# Install Elasticsearch
ENV ELASTICSEARCH_VER 7.1.1
RUN wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ELASTICSEARCH_VER}-amd64.deb"
RUN dpkg -i --force-confnew elasticsearch-${ELASTICSEARCH_VER}-amd64.deb
# RUN until curl --silent -XGET --fail http://localhost:9200; do printf '.'; sleep 1; done


# Make port 80 available to the world outside this container
EXPOSE 80 9200

# Define environment variable
ENV VERSION 1

# Run app when the container launches
CMD ["python", "-m", "qas.adam", "-v"]
