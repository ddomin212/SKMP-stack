import json
import logging
import os
import time

import requests
from kafka.producer import KafkaProducer

if os.getenv("MODE") != "prod":
    from dotenv import load_dotenv

    load_dotenv()

KAFKA_BOOTSTRAP_SERVERS_CONS = "kafka1:19092"
KAFKA_TOPIC_NAME_CONS = "test-topic"

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.WARNING
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

json_message = None
city_name = None
temperature = None
humidity = None
openweathermap_api_url = None
appid = None


def get_weather_detail(openweathermap_api_endpoint):
    api_response = requests.get(openweathermap_api_endpoint)
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


while True:
    for i in ["London", "Prague", "Tokyo", "New+York", "Mlada+Boleslav"]:
        openweathermap_api_url = (
            "http://api.openweathermap.org/data/2.5/weather?q="
            + i
            + "&appid="
            + os.getenv("OPENWEATHERMAP_API_KEY")
        )
        json_message = get_weather_detail(openweathermap_api_url)
        logging.warning("Message to be sent: " + str(json_message))
        producer.send(KAFKA_TOPIC_NAME_CONS, json_message)
        print("waiting for 2 seconds")
        time.sleep(2)
