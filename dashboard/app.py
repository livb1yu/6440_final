'''
Written by Chanho Lim clim66@gatech.edu for CS6440
'''

import streamlit as st
import pandas as pd
import wfdb
import numpy as np
from preprocessing.noise_reduction import NoiseReducer
from preprocessing.signal_normalization import SignalNormalizer
from detection.arrhythmia_detector import ArrhythmiaDetector
#from detection.ml_model import ArrhythmiaClassifier  # commented out for now
from visualization import ECGVisualizer
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def load_record_list():
    # Load record_list.csv and sample 10,000 rows for performance
    df = pd.read_csv('../sampled_record_list.csv')
    # df = df.sample(n=10000, random_state=42)
    return df

def load_machine_measurements():
    # Load the additional machine measurements CSV.
    df = pd.read_csv('../sampled_machine_measurements.csv')
    return df

def visualize_record_distribution(df, fig):
    subject_counts = df['subject_id'].value_counts()
    signal_count_distribution = subject_counts.value_counts().sort_index()
    
    fig.add_trace(go.Bar(
        x=signal_count_distribution.index.astype(str),
        y=signal_count_distribution.values,
        marker=dict(color='blue')
    ))
    fig.update_layout(
        title='Distribution of ECG Signal Count per Subject',
        xaxis_title='Number of ECG Signals',
        yaxis_title='Number of Subjects',
        xaxis_tickangle=-45
    )

def main():
    st.title("MIMIC-IV ECG Record Browser")

    # Load the record list and machine measurements data
    record_df = load_record_list()
    machine_df = load_machine_measurements()

    st.sidebar.header("Record Selection")

    unique_subjects = sorted(record_df['subject_id'].unique())
    selected_subject = st.sidebar.selectbox("Select Subject ID", unique_subjects)

    subject_records = record_df[record_df['subject_id'] == selected_subject].sort_values('ecg_time')

    st.sidebar.subheader(f"Records for Subject {selected_subject}")
    selected_record = st.sidebar.selectbox(
        "Select ECG Record", 
        subject_records['path'].tolist(),
        format_func=lambda x: f"Record at {subject_records[subject_records['path'] == x]['ecg_time'].values[0]}"
    )

    if selected_record:
        try:
            # Read the selected ECG record
            record = wfdb.rdrecord(selected_record)
            signal_data = record.p_signal
  
            # Process the signal
            noise_reducer = NoiseReducer()
            normalizer = SignalNormalizer()
            processed_signal = noise_reducer.process(signal_data)
            normalized_signal = normalizer.normalize(processed_signal)
            
            # Perform arrhythmia detection (using a default lead, e.g., lead II)
            detector = ArrhythmiaDetector()
            lead_ii_results = detector.detect_arrhythmia(normalized_signal)
            
            # Visualize the 12-lead ECG
            visualizer = ECGVisualizer()
            fig = visualizer.create_12_lead_plot(normalized_signal, lead_ii_results['peaks'])
            st.plotly_chart(fig)
            
            # Display analysis results
            st.subheader("Analysis Results")
            st.write(f"Arrhythmia Detected: {lead_ii_results['is_arrhythmic']}")
            st.write(f"Confidence: {lead_ii_results['confidence']:.2f}")
            
            # Pull and display machine measurements for the selected record.
            # Here, we assume the machine measurements CSV contains a column 'path' 
            # that matches the record paths from the record_list.
            record_measurements = machine_df[machine_df['path'] == selected_record]
            if not record_measurements.empty:
                st.subheader("Machine Measurements for Selected Record")
                st.dataframe(record_measurements)
            else:
                st.write("No machine measurements available for this record.")
            
        except Exception as e:
            st.error(f"Error processing record: {e}")

    # Optional: Display overall distribution of records per subject.
    st.subheader("ECG Records Distribution")
    fig = go.Figure()
    visualize_record_distribution(record_df, fig)
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
