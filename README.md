# IoT Health Intelligence - Water Quality Surveillance

[![Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20MQTT%20%7C%20MongoDB-blue)](https://github.com/desireeye/iot-health-intelligent)

A full-stack IoT Predictive Health Intelligence system designed for real-time water quality monitoring and outbreak prediction. This system simulates IoT sensor networks, processes edge data, facilitates real-time alerts, and visualizes trends via a modern dashboard.

## 🏗 System Architecture

The system consists of the following microservices orchestrated via Docker Compose:

1.  **IoT Simulator**: Generates realistic water quality sensor data (pH, Turbidity, TDS, Temp) and publishes to MQTT.
2.  **Edge Node**: Subscribes to raw sensor topics, performs noise filtering and local anomaly detection, and forwards processed data.
3.  **MQTT Broker (Mosquitto)**: Handles message exchange between devices and the backend.
4.  **Backend (FastAPI)**: Consumes data, stores it in MongoDB (TimeSeries), manages alerts, and exposes REST APIs.
5.  **Database (MongoDB)**: Stores high-velocity sensor time-series data and alert logs.
6.  **Cache/Stream (Redis)**: Used for caching and real-time pub/sub features.
7.  **Frontend (React + Vite)**: Real-time dashboard for monitoring trends and alerts.

## 🚀 Getting Started

### Prerequisites

-   **Docker** & **Docker Compose** installed.

### Installation & Run

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/desireeye/iot-health-intelligent.git
    cd iot-health-intelligent
    ```

2.  **Start the Services**:
    ```bash
    docker-compose up --build
    ```
    *This may take a few minutes for the first build (installing Python ML libraries + Node modules).*

3.  **Access the Application**:
    -   **Web Dashboard**: [http://localhost:3000](http://localhost:3000)
    -   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Mongo Express** (if enabled): [http://localhost:8081](http://localhost:8081)

## 📡 Features

### Backend (FastAPI)
-   **Async MongoDB (Beanie)**: Efficient storage of time-series sensor data.
-   **MQTT Integration**: Direct subscription to sensor topics.
-   **ML Ready**: Structure used for predictive outbreak models (`scikit-learn`).

### Frontend (React + Tailwind)
-   **Real-time Charts**: Visualizes pH and Turbidity trends using `recharts`.
-   **Live Alerts**: Displays anomaly alerts instantly.
-   **Responsive Design**: Modern UI with dark/light mode adaptable components.

### IoT Components
-   **Simulator**: Simulates 5 nodes with random walk algorithms for realistic data drift and occasional "spikes" (anomalies).
-   **Edge Processing**: Implements Moving Average filters and simple threshold-based anomaly detection before data reaches the cloud.

## 📂 Project Structure

```
iot-health-intelligent/
├── backend/            # FastAPI Application
├── frontend/           # React + Vite Dashboard
├── iot-simulator/      # Python Sensor Simulator
├── edge-processing/    # Edge Logic (Filtering/Anomalies)
├── infra/              # Configs (Mosquitto, etc.)
├── ml/                 # Machine Learning Models
└── docker-compose.yml  # Orchestration
```
<img width="2965" height="8192" alt="image" src="https://github.com/user-attachments/assets/ba12d9cf-354f-4712-a4c8-d2a906f1ed6d" />

## 🛡 License

MIT License
