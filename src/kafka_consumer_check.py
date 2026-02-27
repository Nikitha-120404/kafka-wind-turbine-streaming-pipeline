# -------------------------------------------------------------
# Kafka Consumer - Data Verification
# -------------------------------------------------------------
# This consumer is used ONLY to check whether data is being
# correctly received from the Kafka topic.
#
# Flow:
# Kafka Broker  -->  Kafka Consumer (print messages)
# -------------------------------------------------------------

# Import Kafka Consumer from Confluent Kafka library
from confluent_kafka import Consumer

# -------------------------------------------------------------
# Kafka Configuration
# -------------------------------------------------------------

# Consumer configuration dictionary
conf = {
    'bootstrap.servers': '192.168.59.128:9092',   # Kafka broker IP + port
    'group.id': 'windturbine-consumer-group',     # Consumer group ID
    'auto.offset.reset': 'earliest'               # Read from beginning if no offset exists
}

# Create Kafka Consumer instance
consumer = Consumer(conf)

# -------------------------------------------------------------
# Topic Subscription
# -------------------------------------------------------------

# Subscribe to Kafka topic
consumer.subscribe(['windturbine-data'])

print("Subscribed! Listening for messages...")

# -------------------------------------------------------------
# Message Consumption Loop
# -------------------------------------------------------------

try:
    # Infinite loop to continuously poll messages
    while True:

        # Poll Kafka (wait up to 1 second)
        msg = consumer.poll(1.0)

        if msg is None:
            # No message received → continue polling
            continue

        if msg.error():
            # Print consumer error and continue
            print("Consumer error: {}".format(msg.error()))
            continue

        # Print received message
        print(f"Received message: {msg.value().decode('utf-8')}")

# -------------------------------------------------------------
# Graceful Shutdown
# -------------------------------------------------------------

except KeyboardInterrupt:
    pass

finally:
    # Close consumer properly
    consumer.close()
    print("Consumer closed.")

# END OF CODE
