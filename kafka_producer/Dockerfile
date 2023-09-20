FROM python:3.10.7
WORKDIR /app
COPY . /app
RUN pip install kafka-python requests python-dotenv
CMD ["python", "kafka_producer.py"]