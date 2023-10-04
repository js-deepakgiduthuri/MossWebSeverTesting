# Use an official Python runtime as a parent image
FROM arm32v7/python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
# (Modify this if your script needs a different port)
EXPOSE 5002

# Define environment variable (if needed)
# ENV VARIABLE_NAME variable_value

# Run main.py when the container launches
CMD ["python", "test4.py"]
