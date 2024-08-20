# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir torch transformers && pip install accelerate && pip install openai

# # Copy the Python script into the container
# COPY octopus_v4_chatbot.py /app/

# # Run the script when the container launches
# CMD ["python", "octopus_v4_chatbot.py"]

# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt  && \ 
    pip install --no-cache-dir --upgrade openai

# Copy project
COPY . /app/

# Run the application
CMD ["python", "open-ai-app.py"]