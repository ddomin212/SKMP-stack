import json
import logging
import os
import time

import requests
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_SERVER = "kafka1:19092"
KAFKA_TOPIC = "test-topic"


def init_producer():
    """
    Create Kafka producer
    :return: Kafka producer object
    """
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        )
        return producer
    except KafkaError as ex:
        logging.error("Failed to create producer: %s", str(ex))
        exit(1)


def get_weather_detail(city_name):
    """
    Get weather detail from OpenWeatherMap API
    :param city_name: City name
    :return: dictionary with weather data
    """
    weather_url = (
        "http://api.openweathermap.org/data/2.5/weather?q="
        + city_name
        + "&appid="
        + os.getenv("OPENWEATHERMAP_API_KEY")
    )
    api_response = requests.get(weather_url, timeout=10)
    json_data = api_response.json()
    city_name = json_data["name"]
    temperature = json_data["main"]["temp"]
    humidity = json_data["main"]["humidity"]
    json_message = {
        "CityName": city_name,
        "Temperature": temperature,
        "Humidity": humidity,
        "CreationTime": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return json_message
