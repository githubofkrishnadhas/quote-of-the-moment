# using python 3.11 image as base image
FROM python:3.11.8-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv & install dependencies using pipenv
RUN pip install pipenv && pipenv install --deploy --system

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=quotes.py

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]