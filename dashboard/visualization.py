'''
Written by Chanho Lim clim66@gatech.edu for CS6440
'''

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
class ECGVisualizer:
    def __init__(self):
        self.fig = None

    def create_12_lead_plot(self, ecg_data, peaks=None):
        """Create a 12‑lead ECG plot with corrected x-axis and line properties."""
        lead_names = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 
                      'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
        self.fig = make_subplots(rows=12, cols=1, 
                                 subplot_titles=lead_names,
                                 vertical_spacing=0.02)

        for i in range(12):
            # Create an x-axis using the sample indices
            x_values = np.arange(ecg_data[i].shape[0])
            peak = peaks[i]
            # Plot the ECG signal with a thinner line for clarity
            self.fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=ecg_data[i],
                    mode='lines',
                    name=lead_names[i],
                    line=dict(width=1)
                ),
                row=i+1, col=1
            )
            
            # If peaks are provided, plot them as red markers
            if peaks is not None:
                self.fig.add_trace(
                    go.Scatter(
                        x=x_values[peaks[i]],
                        y=ecg_data[i][peaks[i]],
                        mode='markers',
                        name=f'Peaks {lead_names[i]}',
                        marker=dict(color='red', size=3)
                    ),
                    row=i+1, col=1
                )
        
        self.fig.update_layout(
            height=1200,
            showlegend=False,
            xaxis_title="Samples",
            yaxis_title="Amplitude"
        )
        return self.fig

