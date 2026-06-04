FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN apt-get update && apt-get install -y \
  chromium \
  chromium-driver \
  fonts-liberation \
  libnss3 \
  libxss1 \
  libasound2 \
  libgbm1 \
  libgtk-3-0 \
  ca-certificates
RUN pip install --no-cache-dir -r requirements.txt

COPY . .