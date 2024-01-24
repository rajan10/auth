# Use an official Python runtime with os buster as a parent image # alpine image(raw)
FROM python:3.10-buster

# just fetches the latest package data into Docker image during build time. it 
# doesn't install anything but prepares the img so later package installs can get newest version
RUN  apt update 

#copy local requirements.txt file to the linux  /usr/src directory  
COPY ./requirements.txt /usr/src

#update pip from the linux os
RUN pip install --upgrade pip

# install the requirements
RUN pip install -r /usr/src/requirements.txt

# for worke thread pool from module gunicorn
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /usr/src

# Set the working directory to /app
WORKDIR /usr/src

# Make port 80 available to the world outside this container
EXPOSE 5000
# make executable
RUN chmod +x /usr/src/entrypoint.sh

# Run app.py when the container launches
ENTRYPOINT [ "./entrypoint.sh" ]
