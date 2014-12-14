#!/usr/bin/env python
from kafka import KafkaClient, SimpleConsumer
import time, sys

def measure_single(consumer):
    count = 0
    start = time.time()
    try:

        for entry in consumer:
            if (time.time() - start) > 1:
                return count
            count += 1
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: ./kafka_mps.py <topic>"
        sys.exit(1)

    kafka = KafkaClient("localhost:9092")
    consumer = SimpleConsumer(kafka, "kafka_mps", ' '.join(sys.argv[1:]))

    while True:
        sys.stdout.write("\rCurrent Messages/second: %s" % measure_single(consumer))
        sys.stdout.flush()


