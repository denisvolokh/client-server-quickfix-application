import redis
import time

if __name__ == "__main__":
    client = redis.Redis("redis")

    while True:
        client.publish("internal", "ping")

        time.sleep(10)