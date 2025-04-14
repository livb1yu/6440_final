'''
Written by Chanho Lim clim66@gatech.edu for CS6440
'''

import numpy as np

class SignalNormalizer:
    def __init__(self):
        self.mean = None
        self.std = None

    def mean_normalize(self, data):
        """Z-score normalization"""
        self.mean = np.mean(data, axis=0)
        self.std = np.std(data, axis=0)
        return (data - self.mean) / self.std

    def minmaxnorm(self, signal, new_min=0, new_max=1):
        signal = np.asarray(signal)
        min_val, max_val = np.min(signal), np.max(signal)
        range_val = max_val - min_val
        if range_val < 1e-10:
            return np.full(signal.shape, new_min)
        return (signal - min_val) * (new_max - new_min) / range_val + new_min
    
    def normalize(self, signal):
        return np.array([self.minmaxnorm(x) for x in signal])
    
    def denormalize(self, data):
        """Reverse normalization"""
        if self.mean is None or self.std is None:
            raise ValueError("Normalizer not fitted")
        return (data * self.std) + self.mean