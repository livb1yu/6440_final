'''
Written by Chanho Lim clim66@gatech.edu for CS6440
'''
import neurokit2 as nk
import numpy as np
from scipy import signal


class ArrhythmiaDetector:
    def __init__(self, sampling_rate=500):
        self.sampling_rate = sampling_rate

    def detect_qrs(self, ecg_signal):
        """Detect QRS complexes using a simplified Pan-Tompkins algorithm.
           Expects a 1D ECG signal.
        """
        # filtered = signal.savgol_filter(ecg_signal, 15, 4)
        # squared = filtered ** 2
        # integrated = np.convolve(squared, np.ones(30)/30, mode='same')
        # peaks, _ = signal.find_peaks(integrated, distance=50)
        signals, info = nk.ecg_process(ecg_signal, sampling_rate=self.sampling_rate)
        peaks = info["ECG_R_Peaks"]
        return peaks

    def calculate_rr_intervals(self, peaks):
        """Calculate R-R intervals based on detected QRS peaks."""
        rr_intervals = np.diff(peaks) / self.sampling_rate
        return rr_intervals

    def detect_arrhythmia(self, ecg_signal):
        """Detect arrhythmia from a 12-lead ECG signal.
        
           If the input signal has shape (12, 5000), it selects lead II
           (assumed to be the second lead, index 1) by default.
        """
        # Check if the signal is multi-dimensional (e.g., 12 leads)
        # if len(ecg_signal) > 1:
        #     # Use lead II if available (index 1), otherwise use the first lead.
        #     if ecg_signal.shape[0] > 1:
        #         selected_signal = ecg_signal[1]
        #     else:
        #         selected_signal = ecg_signal[0]
        # else:
        #     selected_signal = ecg_signal

        peaks = [self.detect_qrs(ecg_signal[1]) for i in range(len(ecg_signal))]
        rr_intervals = self.calculate_rr_intervals(peaks[1])
        rr_std = np.std(rr_intervals)
        
        return {
            'peaks': peaks,
            'is_arrhythmic': rr_std > 0.15,
            'confidence': 1 - min(rr_std, 0.5) / 0.5
        }