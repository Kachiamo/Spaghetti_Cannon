FROM python:3.9.18-alpine

# Install dependencies
RUN apk update && \
apk upgrade && \
apk add --no-cache \
postgresql \
libpq \
bash

# Create /usr/src/app dir
RUN mkdir -p /usr/src/app && mkdir -p /usr/web
WORKDIR /usr/src/app

# Copy requirements
COPY requirements.txt .

# Pip install requirements
RUN pip3 install --no-cache-dir --upgrade pip==23.1.2 && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy project files
COPY webapp ./

#Production image
ENV PYTHONPATH=.

WORKDIR /usr/src/app
CMD ["./run.sh"]
