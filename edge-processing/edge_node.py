import json
import os
import paho.mqtt.client as mqtt
import numpy as np
from collections import deque

# Configuration
BROKER = os.getenv("BROKER", "localhost")
PORT = 1883
SUB_TOPIC = "sensors/water_quality/+"
PUB_TOPIC_BASE = "processed/water_quality"

# Simple state for moving average filter
history = {}
WINDOW_SIZE = 5

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Edge Node Connected with result code {rc}")
    client.subscribe(SUB_TOPIC)

def moving_average(sensor_id, new_val, param):
    key = f"{sensor_id}_{param}"
    if key not in history:
        history[key] = deque(maxlen=WINDOW_SIZE)
    
    history[key].append(new_val)
    return round(sum(history[key]) / len(history[key]), 2)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        sensor_id = payload.get("sensor_id")
        
        # 1. Noise Filtering (Edge Compute)
        # We only filter pH and Turbidity for now
        payload['ph'] = moving_average(sensor_id, payload['ph'], 'ph')
        payload['turbidity'] = moving_average(sensor_id, payload['turbidity'], 'turbidity')
        
        # 2. Anomaly Detection (Simple Threshold at Edge)
        is_anomalous = False
        if payload['ph'] < 6.5 or payload['ph'] > 8.5:
            is_anomalous = True
        
        payload['is_anomalous'] = is_anomalous
        
        # 3. Gateway / Forwarding
        # Forward to processed topic
        pub_topic = f"{PUB_TOPIC_BASE}/{sensor_id}"
        client.publish(pub_topic, json.dumps(payload))
        print(f"Processed & Forwarded: {sensor_id} -> Anomaly: {is_anomalous}")
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping Edge Node...")

if __name__ == "__main__":
    main()
