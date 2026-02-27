# Kafka Wind Turbine Streaming Pipeline 🚀

## 📌 Project Overview
This project simulates real-time IoT wind turbine sensor data and builds an end-to-end streaming data pipeline using **Apache Kafka** and **TimescaleDB**.

The pipeline streams simulated turbine sensor data → Kafka Producer → Kafka Broker → Kafka Consumer → TimescaleDB for real-time time-series storage and analytics.

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
Continuous Aggregates & Time-Series Analytics

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

## ✨ Features

- Real-time IoT wind turbine data simulation
- Kafka Producer and Consumer implementation
- Streaming ingestion into TimescaleDB
- Manual Kafka offset commit after successful DB insert
- TimescaleDB hypertable for time-series data
- Continuous aggregate for 5-minute analytics
- Compression and retention policies

---

## How to Run

### 1️⃣ Start Kafka Broker
Make sure Kafka server is running.

### 2️⃣ Generate Sensor Data
```bash
python wind_turbine_sensorlog.py
3️⃣ Send Data to Kafka
python kafka_producer.py
4️⃣ Verify Kafka Messages (Optional)
python kafka_consumer_check.py
5️⃣ Stream Data into TimescaleDB
python kafka_consumer_to_timescaledb.py
6️⃣ Setup TimescaleDB

Run the SQL file:

sql/timescaledb_queries.sql
📊 Sample Output

Sample streaming output is available here:

output/wind_turbine_streamdata.csv
👩‍💻 Author

Nikitha
