import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# 1. Generate Synthetic Training Data
def generate_dataset(n_samples=5000):
    np.random.seed(42)
    data = []
    
    for _ in range(n_samples):
        # Normal conditions
        ph = np.random.normal(7.2, 0.4)
        turbidity = np.random.normal(3.0, 1.5)
        temp = np.random.normal(25, 2)
        tds = np.random.normal(300, 50)
        label = 0 # Safe
        
        # Anomaly / Outbreak Precursors
        if np.random.random() < 0.2:
            case_type = np.random.choice(['acidic', 'basic', 'high_turbidity', 'contamination'])
            
            if case_type == 'acidic':
                ph = np.random.normal(5.5, 0.5)
                label = 2 # Danger
            elif case_type == 'basic':
                ph = np.random.normal(9.0, 0.5)
                label = 1 # Warning
            elif case_type == 'high_turbidity':
                turbidity = np.random.normal(15.0, 5.0)
                label = 1 # Warning
            elif case_type == 'contamination':
                ph = np.random.normal(6.5, 0.3)
                turbidity = np.random.normal(25.0, 5.0)
                tds = np.random.normal(500, 50)
                label = 2 # High Risk / Outbreak
        
        data.append([ph, turbidity, temp, tds, label])
        
    df = pd.DataFrame(data, columns=['ph', 'turbidity', 'temperature', 'tds', 'risk_level'])
    return df

def train():
    print("Generating synthetic dataset...")
    df = generate_dataset()
    
    X = df[['ph', 'turbidity', 'temperature', 'tds']]
    y = df['risk_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    print("Training Random Forest Model...")
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/water_quality_rf.pkl')
    print("Model saved to ml/models/water_quality_rf.pkl")

if __name__ == "__main__":
    train()
