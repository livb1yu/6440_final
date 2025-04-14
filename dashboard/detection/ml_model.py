from sklearn.ensemble import RandomForestClassifier
import numpy as np

class ArrhythmiaClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        
    def extract_features(self, ecg_signal):
        """Extract basic features from ECG signal"""
        return np.array([
            np.mean(ecg_signal),
            np.std(ecg_signal),
            np.max(ecg_signal),
            np.min(ecg_signal),
            np.median(ecg_signal)
        ]).reshape(1, -1)

    def predict(self, ecg_signal):
        """Predict arrhythmia (dummy implementation)"""
        features = self.extract_features(ecg_signal)
        # For prototype, return dummy prediction
        return {'prediction': 'Normal', 'confidence': 0.95}