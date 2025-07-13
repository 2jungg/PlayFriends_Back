# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8080

# Run uvicorn when the container launches
# The PORT environment variable is automatically set by Cloud Run.
CMD ["/bin/sh", "-c", "python scripts/seed_db.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
