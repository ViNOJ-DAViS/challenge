# Dockerfile, Image, Container
FROM python:3.8

ADD README .
ADD challenge_part1.py .
ADD challenge_part2.py .

RUN pip install websockets pandas

CMD [ "cat", "README"]
