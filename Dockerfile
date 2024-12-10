# Use the official Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /user-service

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the service port
EXPOSE 8081

# Set the command to run the application
CMD ["python", "app.py"]
