# Use Python base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for templates if it doesn't exist
RUN mkdir -p templates

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]