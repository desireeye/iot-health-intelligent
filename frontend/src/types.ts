export interface SensorReading {
    _id?: string;
    sensor_id: string;
    timestamp: string;
    ph: number;
    turbidity: number;
    temperature: number;
    tds: number;
    is_anomalous: boolean;
}

export interface Alert {
    timestamp: string;
    severity: "INFO" | "WARNING" | "CRITICAL";
    risk_score: number;
    message: string;
    status: string;
}
