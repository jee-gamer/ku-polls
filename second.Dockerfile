FROM python:3-alpine

ARG SECRET_KEY
ARG ALLOWED_HOSTS=localhost,127.0.0.1,::1,testserver

WORKDIR /app/polls

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV TIME_ZONE=Asia/Bangkok

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
