# Dockerfile

# Step 1: Use an official Python runtime as a parent image.
FROM python:3.9-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Install system dependencies required for building Python packages.
# 'build-essential' and 'cmake' are needed to compile C++ extensions for libraries like llama-cpp-python.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake

# Step 4: Copy the dependencies file first to leverage Docker caching.
COPY requirements.txt .

# Step 5: Upgrade pip and install Python dependencies with a longer timeout.
# We upgrade pip first and add a --timeout flag to make the installation more resilient to network issues.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=100 -r requirements.txt

# Step 6: Copy the rest of the project files.
COPY . .

# Step 7: Expose the port that Gunicorn will run on.
EXPOSE 5000

# Step 8: Use Gunicorn as the production-ready WSGI server.
# 'flask run' is for development only. Gunicorn is a proper production server.
# It runs the 'app' instance from the 'app.py' file.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]