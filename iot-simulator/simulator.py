import time
import json
import random
import os
import paho.mqtt.client as mqtt
import numpy as np

# Configuration
BROKER = os.getenv("BROKER", "localhost")
PORT = 1883
TOPIC_BASE = "sensors/water_quality"
NUM_DEVICES = 5

def generate_sensor_data(sensor_id):
    """
    Simulates water quality parameters with realistic ranges and specific noise profiles.
    """
    # Base values + Random Walk for drift
    # In a real sim we would maintain state, here we do stateless for simplicity + noise
    base_ph = 7.0 + random.uniform(-0.5, 0.5)
    base_turbidity = 5.0 # NTU
    
    # Add events occasionally
    if random.random() < 0.05:
        # Coliform spike event
        base_ph = 6.5
        base_turbidity = 50.0
    
    data = {
        "sensor_id": sensor_id,
        "timestamp": time.time(),
        "ph": round(max(0, min(14, np.random.normal(base_ph, 0.1))), 2),
        "turbidity": round(max(0, np.random.normal(base_turbidity, 2.0)), 2),
        "temperature": round(np.random.normal(25.0, 1.0), 1),
        "tds": round(max(0, np.random.normal(300, 10)), 0),
        "battery_level": round(random.uniform(80, 100), 1)
    }
    return data

def main():
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    
    try:
        client.connect(BROKER, PORT, 60)
        print(f"Connected to MQTT Broker at {BROKER}:{PORT}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    client.loop_start()

    try:
        while True:
            for i in range(1, NUM_DEVICES + 1):
                device_id = f"node_{i:03d}"
                payload = generate_sensor_data(device_id)
                topic = f"{TOPIC_BASE}/{device_id}"
                
                client.publish(topic, json.dumps(payload))
                print(f"Published to {topic}: {payload}")
                
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping simulator...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
