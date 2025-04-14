'''
Written by Chanho Lim clim66@gatech.edu for CS6440
'''

import numpy as np
from scipy import signal

class NoiseReducer:
    def __init__(self, sampling_rate=500):
        self.sampling_rate = sampling_rate
    
    def crop_initial_noise(signal, duration):
        fs = self.sampling_rate
        start_idx = int(fs * duration)
        return signal[start_idx:] if start_idx < len(signal) else signal

    def standardize_signal_length(signal, target_length):
        if len(signal) > target_length:
            return signal[:target_length]
        elif len(signal) < target_length:
            return np.pad(signal, (0, target_length - len(signal)), 'constant')
        return signal

    def bandpass_filter(self, data, lowcut=3, highcut=25.0, order = 4):
        """Apply bandpass filter to remove noise outside ECG frequency range"""
        nyquist = 0.5 * self.sampling_rate
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = signal.butter(order, [low, high], btype='band')
        return signal.filtfilt(b, a, data)

    def notch_filter(self, data, freq=500.0):
        """Remove power line interference"""
        nyquist = 0.5 * self.sampling_rate
        freq = freq / nyquist
        b, a = signal.iirnotch(freq, 30.0)
        return signal.filtfilt(b, a, data)
    
    def minmaxnorm(self, signal, new_min=0, new_max=1):
        signal = np.asarray(signal)
        min_val, max_val = np.min(signal), np.max(signal)
        range_val = max_val - min_val
        if range_val < 1e-10:
            return np.full(signal.shape, new_min)
        return (signal - min_val) * (new_max - new_min) / range_val + new_min

    def process(self, data):
        """Apply all noise reduction steps"""
        signal = np.array(data).transpose()
        filtered = np.array([self.bandpass_filter(signal[i]) for i in range(12)])
        # filtered = self.minmaxnorm(self.bandpass_filter(signal))
        # filtered = np.array([self.notch_filter(filtered[i]) for i in range(12)])
        return filtered