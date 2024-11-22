FROM python:3-alpine

WORKDIR /app/polls
COPY ../requirements.txt .

# Install dependencies on Docker container
RUN pip install -r requirements.txt

ARG SECRET_KEY
ARG ALLOWED_HOST=localhost,127.0.0.1,::1,testserver

ENV SECRET_KEY=${S70o9icTfLZfmLwW2zNMsPc-F4wg93qiWuyf3tjsSSc4onpAk5CZXDoE5HSEUYQH6-I}
ENV DEBUG=True
ENV ALLOWED_HOSTS='127.0.0.1,localhost'
ENV TIME_ZONE=Asia/Bangkok

COPY .. .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000


CMD [ "./entrypoint.sh" ]
