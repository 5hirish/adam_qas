# Use an official Python runtime as a parent image
FROM python:3.5-jessie

MAINTAINER  Shirish Kadam <shirishkadam35@gmail.com>

# Set the working directory to /app
WORKDIR /adam_qas

# Copy the current directory contents into the container at /app
COPY . /adam_qas

# Install any needed packages specified in requirements.txt
RUN pip install --default-timeout=3000 --trusted-host pypi.python.org -r requirements-docker.txt
RUN python -m spacy download en
RUN python -m spacy download en_core_web_md

# Install Oracle Java
ENV JAVA_VER 8
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

RUN echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" >> /etc/apt/sources.list && \
    echo "deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886 && \
    apt-get update && \
    echo oracle-java${JAVA_VER}-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
    apt-get install -y --force-yes --no-install-recommends oracle-java${JAVA_VER}-installer oracle-java${JAVA_VER}-set-default && \
    apt-get clean && \
    rm -rf /var/cache/oracle-jdk${JAVA_VER}-installer

RUN update-java-alternatives -s java-8-oracle

RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> ~/.bashrc

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Elasticsearch
ENV ELASTICSEARCH_VER 6.1.2

RUN wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ELASTICSEARCH_VER}.deb"
RUN dpkg -i --force-confnew elasticsearch-${ELASTICSEARCH_VER}.deb
#RUN until curl --silent -XGET --fail http://localhost:9200; do printf '.'; sleep 1; done


# Make port 80 available to the world outside this container
EXPOSE 80 9200 9300

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "-m", "qas.adam", "-v"]
