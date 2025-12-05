# syntax=docker/dockerfile:1
FROM python:3.10-alpine
COPY src /code
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
RUN cp .env.example .env
# Run the cron every minute
# TODO: update this to once a day for submission
RUN echo '*  *  *  *  *    python /code/main.py' > /etc/crontabs/root
EXPOSE 5000
CMD crond -f
