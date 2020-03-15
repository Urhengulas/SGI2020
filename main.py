import json
import logging
from time import sleep

from mfrc522 import SimpleMFRC522
from RPi import GPIO

from config import in1, in2, in3, in4
from engine import GPIO, engine1, engine2

# set up logger
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# rfid-reader
reader = SimpleMFRC522()

if __name__ == "__main__":
    engine1.start(100)
    GPIO.output(in1, GPIO.HIGH)
    engine2.start(100)
    GPIO.output(in3, GPIO.HIGH)
    try:
        while(True):
            _, data = reader.read()
            try:
                data_dict = json.loads(data)
                material = data_dict.get("data").get("mat")
                if material == "plastic":
                    # do sth
                    logger.info("plastic")
                else:
                    # do sth else
                    logger.info(f"no plastic, but {material}")
            except json.JSONDecodeError:
                logger.error("json.JSONDecodeError")
    finally:
        engine1.stop()
        engine2.stop()
        GPIO.cleanup()
