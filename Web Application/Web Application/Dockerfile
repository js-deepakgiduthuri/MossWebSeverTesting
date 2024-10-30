# Use an official Python runtime as a parent image
FROM arm32v7/python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add requirements1.txt to the working directory
ADD requirements1.txt /app

# Install any needed packages specified in requirements1.txt
RUN pip install --no-cache-dir -r requirements1.txt

# Add the current directory contents into the container at /app
ADD . /app

# Make port 5055 available to the world outside this container
EXPOSE 5055

# Run app.py when the container launches
CMD ["python", "app.py"]
