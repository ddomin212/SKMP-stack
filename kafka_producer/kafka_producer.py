import logging
import os
import time

from utils import KAFKA_TOPIC, get_weather_detail, init_producer

if os.getenv("MODE") != "prod":
    from dotenv import load_dotenv

    load_dotenv()

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.WARNING
)

producer = init_producer()


while True:  # we need the producer until shutdown
    for city in ["London", "Prague", "Tokyo", "New+York", "Mlada+Boleslav"]:
        json_message = get_weather_detail(city)
        logging.warning("Message to be sent: %s", str(json_message))
        producer.send(KAFKA_TOPIC, json_message)
        time.sleep(2)
