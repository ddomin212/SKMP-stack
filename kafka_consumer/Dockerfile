FROM python:3.10.7
# Set the working directory to /app
WORKDIR /app
#Copy python script for batch
COPY kafka_consumer.py /app/app.py
RUN pip install kafka-python mysql-connector-python
# Define default command
CMD ["python", "app.py"]