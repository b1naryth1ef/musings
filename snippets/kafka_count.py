#!/usr/bin/env python
import sys
from kafka import KafkaClient, SimpleConsumer

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print "Usage: ./kafka_count.py <topic>"
        sys.exit(1)

    kafka = KafkaClient("localhost:9092")
    consumer = SimpleConsumer(kafka, "kafka_count", ' '.join(sys.argv[1:]))
    consumer.seek(-1, 2)

    for item in consumer:
        head = item.offset
        break

    consumer.seek(0, 0)

    count = 0
    for item in consumer:
        count += 1
        if item.offset >= head:
            break

    print "Topic has %s messages" % count
