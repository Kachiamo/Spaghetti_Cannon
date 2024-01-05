FROM python:3.9-slim-bookworm

# Install dependencies
RUN apt update && \
    apt upgrade && \
    apt -y install \
    postgresql \
    libpq-dev \
    python3-sklearn \
    python3-sklearn-lib \
    bash

# Create /usr/src/app dir
RUN mkdir -p /usr/src/app && mkdir -p /usr/web
WORKDIR /usr/src/app

# Copy requirements
COPY requirements.txt .

# Pip install requirements
RUN pip3 install --no-cache-dir --upgrade pip==23.3.2 && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY webapp ./

#Production image
ENV PYTHONPATH=.

WORKDIR /usr/src/app
CMD ["./run.sh"]
