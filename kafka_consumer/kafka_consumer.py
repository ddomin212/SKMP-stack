import json
import logging

import mysql.connector
from kafka import KafkaConsumer

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.WARNING
)
# Kafka broker(s) and topic
bootstrap_servers = "kafka1:19092"
topic_name = "test-topic"


def insert_to_db(json_data):
    # Connect to the database
    conn = mysql.connector.connect(
        host="host.docker.internal",
        port=3306,
        database="weather",
        user="dbadmin",
        password="123",
    )
    sql = "INSERT INTO data (CityName, Temperature, Humidity, CreationTime) VALUES (%s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, list(json_data.values()))

    # Commit the transaction (if applicable)
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()


try:
    # Create KafkaConsumer instance
    consumer = KafkaConsumer(topic_name, bootstrap_servers=bootstrap_servers)
except Exception as ex:
    logging.error(f"Failed to create consumer: {ex}")
    exit(1)

# Continuously poll for new messages
for idx, message in enumerate(consumer):
    # Decode message value assuming it's in UTF-8 format
    message_value = message.value.decode("utf-8")
    json_data = json.loads(message_value)
    insert_to_db(json_data)
    # Print the message key and value
    if idx < 3:
        logging.warning(f"Key: {message.key}, Value: {message_value}")
