# Dockerfile

# Step 1: Use an official Python runtime as a parent image.
FROM python:3.9-slim

# Step 2: Set the working directory inside the container.
WORKDIR /app

# Step 3: Install system dependencies required for building Python packages.
# 'build-essential' provides C/C++ compilers (like gcc) and 'cmake' is a build tool.
# Both are CRITICAL for compiling llama-cpp-python.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake

# Step 4: Copy the dependencies file first to leverage Docker caching.
COPY requirements.txt .

# Step 5: Upgrade pip and install Python dependencies.
# We no longer need the timeout flag as the network issue is solved.
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the model file INTO the container image.
# WARNING: This will make your Docker image VERY LARGE (several GBs)!
COPY ./model /app/model

# Step 7: Copy the rest of the project files.
COPY . .

# Step 8: Expose the port that Gunicorn will run on.
EXPOSE 5000

# Step 9: Use Gunicorn as the production-ready WSGI server.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]