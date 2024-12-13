# syntax=docker/dockerfile:1

# Base Python image
ARG PYTHON_VERSION=3.12.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install Poetry
RUN python -m pip install --upgrade pip && pip install poetry

# Copy project files into the container
COPY . .

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root --only main

# Expose the port the application listens on
EXPOSE 8000

# Run the application
CMD ["python3", "cli.py", "start:prod"]
