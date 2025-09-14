# Dockerfile

# Step 1: Use an official Python runtime as a parent image.
# We'll use a slim version of Python 3.9, which helps keep the final image size small.
FROM python:3.9-slim

# Step 2: Set the working directory inside the container.
# All subsequent commands will be run from the /app directory.
WORKDIR /app

# Step 3: Copy the dependencies file first.
# By copying only requirements.txt initially, we leverage Docker's layer caching.
# This speeds up future builds if the dependencies haven't changed.
COPY requirements.txt .

# Step 4: Install the dependencies.
# Install all the Python libraries listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the project files.
# Copy all the source code from the current local directory into the container's /app directory.
COPY . .

# Step 6: Expose the port that the app runs on.
# This informs Docker that the container listens on port 5000 at runtime.
EXPOSE 5000

# Step 7: Define the command to run the application.
# This command starts the Flask development server.
# The "--host=0.0.0.0" argument is crucial for making the server accessible from outside the container.
CMD ["flask", "run", "--host=0.0.0.0"]