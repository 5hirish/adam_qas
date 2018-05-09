# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /app
WORKDIR /adam_qas

# Copy the current directory contents into the container at /app
ADD . /adam_qas

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install elasticsearch
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.1.2.deb
RUN dpkg -i --force-confnew elasticsearch-6.1.2.deb
RUN service elasticsearch restart
RUN until curl --silent -XGET --fail http://localhost:9200; do printf '.'; sleep 1; done

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "-m", "qas.adam", "-v"]
