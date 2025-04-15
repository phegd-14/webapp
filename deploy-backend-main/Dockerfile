# Build stage for FastAPI
FROM python:3.13-alpine AS builder
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

CMD ["fastapi","run"]