FROM arm32v7/python:3.8-slim-buster

WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Copy your Python script and other necessary files to the container
COPY main.py /app/main.py
COPY template.sh /app/template.sh
COPY modem_autoconnect2.sh /app/modem_autoconnect2.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5010 available to the world outside this container
EXPOSE 5010

# Run the Python script
CMD ["python", "/app/main.py"]
