# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install curl and build-essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory inside the container
WORKDIR /app

# Copy all project files, including README.md, pyproject.toml, poetry.lock, source code
COPY . /app

# Install dependencies (no virtualenv so it installs globally in container)
# --no-root because we dont have __init__.py, dont want to install it as package
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Run the Python script
CMD ["python", "main.py"]