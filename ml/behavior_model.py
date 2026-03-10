import statistics
import numpy as np
from sklearn.ensemble import IsolationForest


def calculate_mean(data):
    return statistics.mean(data) if data else 0


def extract_behavior_features(hold_times, key_intervals, mouse_speeds):
    return {
        "avg_hold_time": calculate_mean(hold_times),
        "avg_key_interval": calculate_mean(key_intervals),
        "avg_mouse_speed": calculate_mean(mouse_speeds)
    }


def train_model(samples):
    if len(samples) < 5:
        return None

    X = np.array([
        [
            s["avg_hold_time"],
            s["avg_key_interval"],
            s["avg_mouse_speed"]
        ]
        for s in samples
    ])

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )

    model.fit(X)
    return model


def predict_sample(model, sample):
    X_new = np.array([[
        sample["avg_hold_time"],
        sample["avg_key_interval"],
        sample["avg_mouse_speed"]
    ]])

    prediction = model.predict(X_new)
    score = model.decision_function(X_new)

    return prediction[0], float(score[0])
