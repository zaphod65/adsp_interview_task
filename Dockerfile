# syntax=docker/dockerfile:1
FROM python:3.10-alpine
COPY src /code
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
RUN cp .env.example .env
# Set up cron to run once a day at 4:00 AM
RUN echo '0 4 * * *    python /code/main.py' > /etc/crontabs/root
CMD crond -f
