import os
import sys

import redis
from dotenv import load_dotenv
from gpiozero import CPUTemperature

load_dotenv()


THRESHOLD = int(os.environ.get("THRESHOLD", 70))

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PASS = os.getenv("REDIS_PASS", "password")


def main():
    cpu = CPUTemperature()
    temp = float(cpu.temperature)

    if temp > THRESHOLD:
        # Publish alert to central notify queue
        r_client = redis.Redis(host=REDIS_HOST, password=REDIS_PASS)
        msg = f"RaspberryPi temperature is high: {temp} C"
        r_client.lpush("notify.queue", msg)
        r_client.shutdown()
        print(msg)


if __name__ == "__main__":
    sys.exit(main())
