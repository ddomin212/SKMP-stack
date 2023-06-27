import json
import logging

import mysql.connector
from kafka import KafkaConsumer
from kafka.errors import KafkaError

KAFKA_SERVER = "kafka1:19092"
KAFKA_TOPIC = "test-topic"


def init_consumer():
    """
    Create Kafka consumer
    :return: Kafka consumer object
    """
    try:
        consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER)
        return consumer
    except KafkaError as ex:
        logging.error("Failed to create consumer: %s", str(ex))
        exit(1)


def insert_to_db(json_data):
    """
    Insert data to MySQL database
    :param json_data: JSON data
    :return: None
    """
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


def decode_message(message):
    """
    Decode message from Kafka consumer
    :param message: Kafka message
    :return: JSON data
    """
    message_value = message.value.decode("utf-8")
    json_data = json.loads(message_value)
    return json_data
