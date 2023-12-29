# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install Poetry
RUN pip install poetry

# Use Poetry to install dependencies
RUN poetry install

# Make port 80 available to the world outside this container
EXPOSE 8501

# Run main.py when the container launches
CMD ["poetry", "run", "streamlit", "run", "main.py"]
