import logging

from utils import decode_message, init_consumer, insert_to_db

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.WARNING
)


consumer = init_consumer()

for idx, message in enumerate(consumer):
    decoded_message = decode_message(message)
    insert_to_db(decoded_message)
    if idx < 5:
        logging.warning(
            "Key: %s, Value: %s", message.key, str(decoded_message)
        )
