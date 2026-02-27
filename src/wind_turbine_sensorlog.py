# -------------------------------------------------------------
# Wind Turbine Sensor Data Generator (IoT Simulation)
# -------------------------------------------------------------
# This script continuously generates simulated wind turbine
# sensor data and writes it into a log file as JSON lines.
#
# Each line in wind_turbine.log = one turbine record.
# This file will later be read by the Kafka producer.
# -------------------------------------------------------------

# Import necessary libraries
import json                     # Convert Python dict to JSON string
import random                   # Generate random sensor values
import time                     # Add delay between generations
from datetime import datetime   # Add timestamp to each record
import os                       # Used only to check working directory

# Path to the log file where simulated data will be stored
log_file_path = "wind_turbine.log"

# -------------------------------------------------------------
# Function: generate_data()
# Generates one sensor record for a given turbine
# -------------------------------------------------------------
def generate_data(turbine_id):
    return {
        "Turbine_ID": f"Turbine_{turbine_id}",      # Unique turbine ID
        "Nacelle_Position": round(random.uniform(0, 360), 2),
        "Wind_direction": round(random.uniform(0, 360), 2),
        "Ambient_Air_temp": round(random.uniform(-30, 45), 2),
        "Bearing_Temp": round(random.uniform(10, 70), 2),
        "BladePitchAngle": round(random.uniform(0, 210), 2),
        "GearBoxSumpTemp": round(random.uniform(20, 130), 2),
        "Generator_Speed": round(random.uniform(40, 60), 2),
        "Hub_Speed": random.randint(1, 5),
        "Power": round(random.uniform(50, 1500), 2),
        "Wind_Speed": round(random.uniform(2, 25), 2),
        "GearTemp": round(random.uniform(50, 350), 2),
        "GeneratorTemp": round(random.uniform(25, 150), 2),
        "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# -------------------------------------------------------------
# Main loop: continuous data generation
# -------------------------------------------------------------
try:
    while True:

        # Simulate data for 12 turbines
        for turbine_id in range(1, 13):

            # Generate sensor data
            data = generate_data(turbine_id)

            # Append JSON record into log file
            with open(log_file_path, "a") as logfile:
                logfile.write(json.dumps(data) + "\n")

            # Small delay between each turbine
            time.sleep(0.5)

        # One full cycle completed
        print("One round of turbine data written...")
        time.sleep(2)

# Graceful shutdown when Ctrl + C is pressed
except KeyboardInterrupt:
    print("Data generation stopped.")

# Check current working directory (useful for debugging file path)
print(os.getcwd())
