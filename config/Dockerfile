# Use a Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install Flask and Werkzeug directly
RUN pip install --no-cache-dir Flask==2.0.3 Werkzeug==2.1.2 boto3==1.24.4 python-keycloak==0.20.0

# Copy the rest of the application code
COPY src /app

# Expose the port Flask is running on
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
