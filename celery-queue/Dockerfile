FROM python:3.9-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    # libtesseract-dev \
    # zlib1g-dev \
    # libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue

RUN pip3 install Pillow
RUN pip3 install -r requirements.txt