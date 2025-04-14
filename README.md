# MIMIC-IV ECG Record Browser

**Author:** Chanho Lim (clim66@gatech.edu)  
**Course:** CS6440

## Overview

The MIMIC-IV ECG Record Browser is an interactive Streamlit application designed to help users browse, analyze, and visualize diagnostic ECG records from the MIMIC-IV database. The app integrates several functionalities:

- **Record Sampling:** Efficiently loads a subset (10,000 samples) of available ECG records.
- **Record Selection:** Allows users to select a subject and a specific ECG record.
- **Signal Processing:** Applies noise reduction and signal normalization.
- **Arrhythmia Detection:** Implements arrhythmia detection (using a simplified Pan-Tompkins approach).
- **ECG Visualization:** Displays 12-lead ECG plots using Plotly.
- **Machine Measurements Integration:** Pulls and displays additional machine measurement details from a supplementary CSV file.
- **Record Distribution:** Visualizes the distribution of ECG signals across subjects.

## Project Structure

```text
├── app.py                             # Main Streamlit application script
├── record_list.csv                    # CSV file containing a list of ECG records (sampled)
├── sampled_machine_measurements.csv   # CSV file with additional machine measurement data
├── preprocessing/
│   ├── noise_reduction.py             # Module for ECG noise reduction
│   └── signal_normalization.py        # Module for ECG signal normalization
├── detection/
│   ├── arrhythmia_detector.py         # Module for arrhythmia detection
│   └── ml_model.py                    # (Optional) Machine learning model for arrhythmia classification
└── visualization/
    └── ECGVisualizer.py               # Module for visualizing ECG signals using Plotly
```



## Installation

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [WFDB](https://www.physionet.org/content/wfdb/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/python/)
- [Matplotlib](https://matplotlib.org/)
- [NumPy](https://numpy.org/)

### Setup Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.gatech.edu/clim66/6440_final.git

2. **Install Required Packages:**

    Install the dependencies using pip:

    ```bash 
    pip install streamlit wfdb pandas plotly matplotlib numpy
    ```

    Alternatively, if a requirements.txt file is provided:
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare Data Files:**

- Place record_list.csv in the appropriate directory as referenced in the code.

- Place sampled_machine_measurements.csv in the same directory as app.py (or update the file path in the code accordingly).

- Place the "files" folder for raw data in the same directory as referenced in the code. 

## Running the Application
From the project directory, run the following command to start the Streamlit app:

```bash 
streamlit run app.py
```
This command will launch the application in your default web browser.


### How to Use
1. **Record Selection:**

    - Use the sidebar to select a subject ID.

    - Choose a specific ECG record for the selected subject. The record’s timestamp is displayed for easy identification.

2. **ECG Processing and Visualization:**

    - The selected ECG record is read using WFDB.

    - The signal undergoes noise reduction and normalization.

    - Arrhythmia detection (typically on lead II) is performed, and results (including a confidence score) are displayed.

    - An interactive 12-lead ECG plot is generated using Plotly.

3. **Machine Measurements:**

    - The app pulls additional machine measurement data for the selected record from sampled_machine_measurements.csv and displays it in a data table.

4. **Record Distribution Visualization:**

    -   A bar chart shows the overall distribution of ECG records per subject.



## License
This project is provided under the MIT License.

## Contact
For questions, suggestions, or issues, please contact Chanho Lim at clim66@gatech.edu.