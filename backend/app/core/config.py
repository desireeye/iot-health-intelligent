from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IoT Health Intelligence"
    MONGODB_URI: str = "mongodb://localhost:27017/iot_health_db"
    REDIS_URI: str = "redis://localhost:6379"
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    
    class Config:
        case_sensitive = True

settings = Settings()
