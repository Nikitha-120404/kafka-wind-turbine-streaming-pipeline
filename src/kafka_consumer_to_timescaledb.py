# -------------------------------------------------------------
# Kafka Consumer -> TimescaleDB (Streaming Ingestion)
# -------------------------------------------------------------
# This script consumes real-time messages from Kafka topic
# and inserts the data into TimescaleDB (PostgreSQL).
#
# Flow:
# Kafka Topic --> Consumer --> TimescaleDB Table
#
# -------------------------------------------------------------

# Import Kafka Consumer from Confluent, PostgreSQL connector, and JSON module
# Install using: pip install psycopg2 confluent_kafka
from confluent_kafka import Consumer
import psycopg2       # PostgreSQL/TimescaleDB connector
import json           # For parsing JSON messages

# ---------------- Kafka Consumer Configuration ----------------

# Kafka broker IP and port
KAFKA_BROKER = "192.168.59.128:9092"

# Kafka topic to subscribe to
TOPIC_NAME = "windturbine-data"

# Unique consumer group ID to manage offset tracking
GROUP_ID = "wind_turbine_consumer_group_v2"

# Kafka consumer configuration dictionary
consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,        # Broker details
    'group.id': GROUP_ID,                     # Consumer group ID
    'auto.offset.reset': 'earliest',          # Start from beginning if no committed offset
    'enable.auto.commit': False               # Manual commit after successful DB insert
}

print("BOOTSTRAP SERVERS =", consumer_conf["bootstrap.servers"])

# Create a Kafka Consumer instance with the config
consumer = Consumer(consumer_conf)

# Subscribe to the desired Kafka topic
consumer.subscribe([TOPIC_NAME])

# ---------------- TimescaleDB Configuration ----------------

# PostgreSQL/TimescaleDB connection details
TIMESCALE_DB_HOST = "localhost"
TIMESCALE_DB_NAME = "postgres"
TIMESCALE_DB_USER = "postgres"
TIMESCALE_DB_PASSWORD = "YOUR_PASSWORD"   # <-- Replace locally, but keep safe for GitHub
TIMESCALE_DB_PORT = 5432

# Establish a connection to the TimescaleDB database
conn = psycopg2.connect(
    host=TIMESCALE_DB_HOST,
    database=TIMESCALE_DB_NAME,
    user=TIMESCALE_DB_USER,
    password=TIMESCALE_DB_PASSWORD,
    port=TIMESCALE_DB_PORT
)

# Create a cursor object for executing SQL commands
cur = conn.cursor()

# Define the table name where data will be inserted
TABLE_NAME = "wind_turbine_streamdata"

print(f"Kafka Consumer started with group {GROUP_ID}... Listening for messages from the beginning...")

# ---------------- Main Message Consumption Loop ----------------

try:
    while True:
        # Poll Kafka for messages with a 1-second timeout
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue  # No message received in this poll cycle

        if msg.error():
            # Handle any Kafka message-level errors
            print(f"Kafka Consumer error: {msg.error()}")
            continue

        try:
            # Decode message from bytes to string
            message_value = msg.value().decode('utf-8')

            # Parse the JSON string into a Python dictionary
            data = json.loads(message_value)

            # SQL insert statement for inserting data into TimescaleDB
            insert_query = f"""
                INSERT INTO {TABLE_NAME} (
                    turbine_id, nacelle_position, wind_direction,
                    ambient_air_temp, bearing_temp, blade_pitch_angle,
                    gearbox_sump_temp, generator_speed, hub_speed,
                    power, wind_speed, gear_temp, generator_temp, timestamp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Execute SQL statement with values from Kafka message
            cur.execute(
                insert_query,
                (
                    data.get('Turbine_ID'),
                    data.get('Nacelle_Position'),
                    data.get('Wind_direction'),
                    data.get('Ambient_Air_temp'),
                    data.get('Bearing_Temp'),
                    data.get('BladePitchAngle'),
                    data.get('GearBoxSumpTemp'),
                    data.get('Generator_Speed'),
                    data.get('Hub_Speed'),
                    data.get('Power'),
                    data.get('Wind_Speed'),
                    data.get('GearTemp'),
                    data.get('GeneratorTemp'),
                    data.get('Timestamp')
                )
            )

            # Commit DB transaction
            conn.commit()

            # Print success message
            print(f"Inserted into TimescaleDB: {data}")

            # Commit Kafka offset only after successful DB insert
            consumer.commit(msg)

        except Exception as e:
            print(f"Error processing message: {e}")
            conn.rollback()  # Avoid partial insert

except KeyboardInterrupt:
    print("Stopping Kafka Consumer...")

finally:
    # Cleanup resources
    consumer.close()
    cur.close()
    conn.close()
    print("All connections closed properly.")

# END OF CODE
