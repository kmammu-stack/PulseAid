import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

MODEL_PATH = "app/ml/model.pkl"
SCALER_PATH = "app/ml/scaler.pkl"

def generate_training_data():
    """
    Generates realistic synthetic training data for disaster prediction.
    In production this gets replaced with real IMD historical data.
    """
    np.random.seed(42)
    n = 1000

    data = {
        # Normal weather conditions
        "rainfall_mm": np.concatenate([
            np.random.uniform(0, 20, 600),    # normal
            np.random.uniform(50, 200, 200),   # heavy rain (flood risk)
            np.random.uniform(0, 10, 200)      # dry (fire/heat risk)
        ]),
        "wind_speed_kmh": np.concatenate([
            np.random.uniform(0, 30, 600),     # normal
            np.random.uniform(20, 60, 200),    # moderate wind
            np.random.uniform(80, 200, 200)    # cyclone level
        ]),
        "pressure_hpa": np.concatenate([
            np.random.uniform(1005, 1020, 600), # normal
            np.random.uniform(990, 1005, 200),  # low pressure (storm)
            np.random.uniform(970, 990, 200)    # very low (cyclone)
        ]),
        "temperature": np.concatenate([
            np.random.uniform(20, 35, 600),    # normal
            np.random.uniform(35, 45, 200),    # extreme heat
            np.random.uniform(15, 25, 200)     # cold front
        ]),
        "humidity": np.concatenate([
            np.random.uniform(40, 70, 600),    # normal
            np.random.uniform(80, 100, 200),   # very humid (flood)
            np.random.uniform(10, 40, 200)     # dry
        ])
    }

    df = pd.DataFrame(data)

    # Create risk labels based on conditions
    def assign_risk(row):
        if row["rainfall_mm"] > 80 and row["humidity"] > 75:
            return 1  # flood risk
        elif row["wind_speed_kmh"] > 80 and row["pressure_hpa"] < 990:
            return 1  # cyclone risk
        elif row["temperature"] > 40 and row["humidity"] < 25:
            return 1  # extreme heat risk
        else:
            return 0  # no major risk

    df["risk"] = df.apply(assign_risk, axis=1)
    return df

def train_model():
    """
    Trains the disaster risk prediction model and saves it to disk.
    """
    print("Training disaster prediction model...")
    df = generate_training_data()

    features = ["rainfall_mm", "wind_speed_kmh", "pressure_hpa", "temperature", "humidity"]
    X = df[features]
    y = df["risk"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )
    model.fit(X_scaled, y)

    # Save model and scaler to disk
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    print(f"Model trained! Accuracy on training data: {model.score(X_scaled, y):.2%}")
    return model, scaler

def load_model():
    """
    Loads model from disk, trains a new one if it doesn't exist yet.
    """
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    else:
        return train_model()

def predict_risk(features: dict):
    """
    Takes a dictionary of weather features and returns:
    - risk_score: float between 0 and 1
    - disaster_type: string describing the likely disaster
    """
    model, scaler = load_model()

    input_data = pd.DataFrame([{
        "rainfall_mm": features["rainfall_mm"],
        "wind_speed_kmh": features["wind_speed_kmh"],
        "pressure_hpa": features["pressure_hpa"],
        "temperature": features["temperature"],
        "humidity": features["humidity"]
    }])

    input_scaled = scaler.transform(input_data)
    risk_score = float(model.predict_proba(input_scaled)[0][1])

    disaster_type = classify_disaster(features)

    return risk_score, disaster_type

def classify_disaster(features: dict) -> str:
    """
    Based on weather features, identifies the most likely disaster type.
    """
    if features["rainfall_mm"] > 80 and features["humidity"] > 75:
        return "FLOOD"
    elif features["wind_speed_kmh"] > 80 and features["pressure_hpa"] < 990:
        return "CYCLONE"
    elif features["temperature"] > 40 and features["humidity"] < 25:
        return "EXTREME_HEAT"
    elif features["rainfall_mm"] < 5 and features["temperature"] > 38:
        return "DROUGHT"
    else:
        return "NONE"

if __name__ == "__main__":
    train_model()