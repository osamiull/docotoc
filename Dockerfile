# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir torch transformers && pip install accelerate

# Copy the Python script into the container
COPY octopus_v4_chatbot.py /app/

# Run the script when the container launches
CMD ["python", "octopus_v4_chatbot.py"]