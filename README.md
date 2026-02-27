# Kafka Wind Turbine Streaming Pipeline 🚀

## 📌 Project Overview

This project demonstrates an **end-to-end real-time data engineering pipeline** built using **Apache Kafka** and **TimescaleDB**.

The system simulates IoT wind turbine sensor data, streams it through Kafka, and stores it inside a TimescaleDB time-series database for analytics and aggregation.

This project showcases real-world concepts used in streaming data engineering:

- Real-time data generation
- Message streaming with Kafka
- Reliable consumption with manual offset commits
- Time-series storage using TimescaleDB
- Continuous aggregates for analytics
- Data compression and retention policies

---

## 🏗️ Architecture


Wind Turbine Sensor Simulation
↓
Kafka Producer
↓
Kafka Broker
↓
Kafka Consumer
↓
TimescaleDB
↓
Continuous Aggregates & Analytics


---

## ⚙️ Technologies Used

- Python
- Apache Kafka
- Confluent Kafka Client
- PostgreSQL / TimescaleDB
- SQL

---

## 📂 Project Structure


kafka-wind-turbine-streaming-pipeline/
│
├── src/
│ ├── wind_turbine_sensorlog.py
│ ├── kafka_producer.py
│ ├── kafka_consumer_check.py
│ └── kafka_consumer_to_timescaledb.py
│
├── sql/
│ └── timescaledb_queries.sql
│
├── output/
│ └── wind_turbine_streamdata.csv
│
├── requirements.txt
└── README.md


---

## ✨ Key Features

- Simulated IoT wind turbine sensor data generation
- Kafka Producer for real-time message publishing
- Kafka Consumer for message validation
- Streaming ingestion into TimescaleDB
- Manual Kafka offset commit after successful database insert
- TimescaleDB hypertable for time-series optimization
- Continuous aggregate for 5-minute analytics
- Compression policy for storage optimization
- Retention policy for long-term data management

---

## 📊 Time-Series Database Design

The project uses TimescaleDB features:

- Hypertables for automatic time partitioning
- Continuous aggregates for fast analytics
- Compression policies for older data
- Data retention policies for cleanup

---

## 📈 Sample Output

Streaming data successfully inserted into TimescaleDB:


output/wind_turbine_streamdata.csv


This file contains sample records generated through the Kafka streaming pipeline.

---

## 🎯 Learning Outcomes

Through this project, I gained hands-on experience with:

- Real-time data streaming pipelines
- Kafka producers and consumers
- Message reliability & offset management
- Time-series database modeling
- Streaming analytics design
- End-to-end data pipeline architecture

---

## 👩‍💻 Author

**Nikitha**
