# Use an official Python slim image as a parent image
FROM python:3.11-slim-bullseye

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /src

# Set the working directory to a dedicated source folder
WORKDIR /src

# Install pip and dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container under the workdir
COPY ./app /src/app
