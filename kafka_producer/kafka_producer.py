import logging
import os
import time

from dotenv import load_dotenv
from utils import KAFKA_TOPIC, get_weather_detail, init_producer

load_dotenv()

print(os.getenv("CITIES"))

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.WARNING
)

producer = init_producer()


while True:  # we need the producer until shutdown
    for city in os.getenv("CITIES").split(";"):
        city = city.strip().replace(" ", "+")
        json_message = get_weather_detail(city)
        logging.warning("Message to be sent: %s", str(json_message))
        producer.send(KAFKA_TOPIC, json_message)
        time.sleep(2)
