# Use the latest Python base image
FROM python:latest

# Update and upgrade the system packages
RUN apt update && apt upgrade -y

# Install required system packages
RUN apt install git curl python3-pip ffmpeg -y

# Update pip to the latest version
RUN pip3 install -U pip

# Copy the requirements file to the root directory
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip3 install -U -r /requirements.txt

# Create a directory for the bot
RUN mkdir /Image-Upload-Bot

# Set the working directory
WORKDIR /Image-Upload-Bot

# Copy the start script to the bot directory
COPY start.sh /Image-Upload-Bot/start.sh

# Set the entry point to run the start script
CMD ["/bin/bash", "/Image-Upload-Bot/start.sh"]
