# Kafka Wind Turbine Streaming Pipeline 🚀

## 📌 Project Overview
This project simulates real-time IoT wind turbine sensor data and builds an end-to-end streaming pipeline using **Apache Kafka** and **TimescaleDB**.

The pipeline streams simulated sensor data through Kafka and stores it inside a TimescaleDB time-series database for real-time analytics.

---

## 🏗️ Architecture

Wind Turbine Sensor Simulation  
⬇  
Kafka Producer  
⬇  
Kafka Broker  
⬇  
Kafka Consumer  
⬇  
TimescaleDB (Hypertable)  
⬇  
Continuous Aggregates & Analytics

---

## ⚙️ Technologies Used

- Python
- Apache Kafka
- Confluent Kafka
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

- Real-time IoT wind turbine data simulation
- Kafka Producer and Consumer implementation
- Streaming ingestion into TimescaleDB
- Manual Kafka offset commit after successful database insert
- TimescaleDB hypertable for time-series optimization
- Continuous aggregate for 5-minute analytics
- Compression and retention policies

---

## 📊 Sample Output

Sample streaming output:


output/wind_turbine_streamdata.csv


---

## 👩‍💻 Author

Nikitha
