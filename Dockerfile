# Dockerfile, Image, Container
FROM python:3.8

ADD binance_data_monitor.py .

RUN pip install websockets

CMD [ "cat", "README"]
