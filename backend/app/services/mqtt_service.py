import json
import asyncio
import paho.mqtt.client as mqtt
from app.core.config import settings
from app.models.sensor_data import SensorReading

# MQTT Client for Backend
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, rc, properties=None):
    print("Backend MQTT Connected")
    client.subscribe("processed/water_quality/+")

def on_message(client, userdata, msg):
    """
    Sync callback from Paho MQTT. Needs to bridge to AsyncIO for Beanie.
    """
    try:
        payload = json.loads(msg.payload.decode())
        # We need to schedule the async insert
        loop = asyncio.get_event_loop()
        loop.create_task(save_reading(payload))
    except Exception as e:
        print(f"Ingestion Error: {e}")

from app.services.inference_service import predictor
from app.models.alert import OutbreakAlert, AlertSeverity

async def save_reading(data: dict):
    try:
        from datetime import datetime
        if isinstance(data.get('timestamp'), float):
             data['timestamp'] = datetime.fromtimestamp(data['timestamp'])
             
        reading = SensorReading(**data)
        
        # 1. AI Inference
        risk_level = predictor.predict_risk(data)
        
        # 2. Check for Alert
        if risk_level > 0:
            severity = AlertSeverity.WARNING if risk_level == 1 else AlertSeverity.CRITICAL
            alert = OutbreakAlert(
                timestamp=reading.timestamp,
                test_station_id=reading.sensor_id,
                severity=severity,
                risk_score=float(risk_level * 50), # Mock score 50 or 100
                prediction_model="RandomForest_v1",
                message=f"Elevated risk detected! Risk Level: {'CRITICAL' if risk_level==2 else 'WARNING'}",
                status="NEW"
            )
            await alert.insert()
            print(f"ALERT GENERATED: {alert.test_station_id} [{severity}]")

        await reading.insert()
    except Exception as e:
        print(f"DB Save Error: {e}")

def start_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    try:
        mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"MQTT Connection Failed: {e}")

def stop_mqtt():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
