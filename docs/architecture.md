# System Architecture: Predictive IoT-Enabled Health Intelligence System

## 1. High-Level Architecture Diagram

```mermaid
graph TD
    subgraph "Sensing Layer (IoT)"
        S1[pH Sensor] -->|Raw Data| MQTT_PUB[MQTT Publisher]
        S2[Turbidity Sensor] -->|Raw Data| MQTT_PUB
        S3[Temp Sensor] -->|Raw Data| MQTT_PUB
        S4[TDS Sensor] -->|Raw Data| MQTT_PUB
    end

    subgraph "Edge Layer (Local Gateway)"
        MQTT_PUB -.->|MQTT| Edge_Node[Edge Gateway]
        Edge_Node -->|Filtering & Aggregation| Edge_Process[Pre-processing Service]
        Edge_Process -->|Clean Data| Cloud_Link[Uplink]
    end

    subgraph "Cloud Layer (Backend & Analytics)"
        Cloud_Link -.->|MQTT/HTTP| MQTT_Broker[Cloud MQTT Broker]
        MQTT_Broker -->|Stream| Ingestion[Ingestion Service]
        Ingestion -->|Hot Data| Redis[Redis Cache/Stream]
        Ingestion -->|Persist| MongoDB[Data Lake (MongoDB)]
        
        MongoDB -->|Training Data| ML_Train[ML Training Pipeline]
        ML_Train -->|Model Artifact| Model_Reg[Model Registry]
        
        Redis -->|Real-time Features| ML_Infer[Inference Service]
        Model_Reg --> ML_Infer
        ML_Infer -->|Risk Score| Alert_Engine[Alert Engine]
    end

    subgraph "Application Layer"
        ML_Infer -->|Predictions| API[FastAPI Gateway]
        MongoDB -->|History| API
        API -->|JSON| Dashboard[React Dashboard]
        Alert_Engine -->|SMS/Email| Authorities[Health Authorities]
    end
```

## 2. Component Details

### 2.1 Sensing Layer
- **Role**: Simulates water quality monitoring stations.
- **Protocol**: MQTT (Lightweight, suitable for low bandwidth).
- **Parameters**: pH (0-14), Turbidity (NTU), Temperature (°C), TDS (ppm), E.coli (CFU/100ml).
- **Implementation**: Python script (`iot-simulator`) generating synthetic data with configurable noise/drift.

### 2.2 Edge Processing Layer
- **Role**: Reduces bandwidth usage and filters sensor noise close to the source.
- **Functions**:
    -   **Noise Filtering**: Moving average or Kalman filter to smooth jitter.
    -   **Anomaly Detection**: Simple threshold-based alerting (e.g., pH > 9).
    -   **Compression**: Batching data before upload if connectivity is poor.
- **Tech**: Python (runs on Raspberry Pi equivalent).

### 2.3 Cloud Analytics Layer (Backend)
- **Ingestion**: Listens to MQTT topics, validates data schema.
- **Storage**:
    -   **Redis**: Temporary storage for real-time streams and "latest state" for dashboard.
    -   **MongoDB**: Persistent storage for historical analysis and model retraining.
- **ML Engine**:
    -   **Random Forest**: For classification (Safe/Caution/Danger).
    -   **LSTM**: For time-series forecasting (Predicting trend for next 24h).
- **Tech**: Python FastAPI, Beanie (ODM), Scikit-learn, PyTorch.

### 2.4 Application Layer (Frontend)
- **Role**: Visualization and Management.
- **Features**:
    -   Real-time gauge/charts.
    -   Geo-spatial map of sensor nodes.
    -   Alert Configuration.
- **Tech**: React, TypeScript, Tailwind CSS, Recharts, Leaflet.

## 3. Data Flow
1.  **Generation**: Sensor simulator generates a reading every 5 seconds.
2.  **Transmission**: Publishes to `sensors/water_quality/{sensor_id}`.
3.  **Edge Processing**: Subscribes, validates, republishes to `processed/{sensor_id}`.
4.  **Ingestion**: Backend worker captures data, saves to Redis (TTL 24h) and MongoDB (Timeseries collection).
5.  **Analysis**: Inference service reads last window (e.g., 10 readings) from Redis -> Predicts Risk.
6.  **Action**: If Risk > Threshold -> Trigger Alert -> Push to Frontend via WebSocket/SSE.

## 4. Security & Privacy
- **Transport**: TLS encryption for MQTT and HTTPs.
- **Auth**: JWT for API access; API Keys for IoT devices.
- **Data**: Data encryption at rest (DB level). Role-Based Access Control (RBAC) in Dashboard.
