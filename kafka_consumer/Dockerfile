FROM python:3.10.7
WORKDIR /app
COPY . /app
RUN pip install kafka-python mysql-connector-python python-dotenv
CMD ["python", "kafka_consumer.py"]