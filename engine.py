import logging

from RPi import GPIO

# set up logger
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(module)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# engine
GPIO.setmode(GPIO.BCM)

in1, in2, ena = 24, 23, 21
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
engine1 = GPIO.PWM(ena, 1000)

in3, in4, enb = 6, 13, 19
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
engine2 = GPIO.PWM(enb, 1000)

if __name__ == "__main__":
    engine1.start(100)
    GPIO.output(in1, GPIO.HIGH)
    logger.info(f"Started engine1 ({engine1})")

    engine2.start(100)
    GPIO.output(in3, GPIO.HIGH)
    logger.info(f"Started engine2 ({engine2})")

    try:
        while(True):
            pass
    finally:
        engine1.stop()
        engine2.stop()
        GPIO.cleanup()
