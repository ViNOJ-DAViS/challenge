# Dockerfile, Image, Container
FROM python:3.8

RUN pip install --upgrade pip

RUN adduser myuser
USER myuser
WORKDIR /home/myuser

RUN pip install websockets pandas

ADD README .
ADD challenge_part1.py .
ADD challenge_part2.py .
