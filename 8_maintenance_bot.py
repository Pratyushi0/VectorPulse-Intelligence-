import joblib
import pandas as pd
from scipy.stats import ks_2samp
import subprocess

# Load the current baseline (from WUSTL-IIoT training)
reference_data = pd.read_csv("WUSTL_IIOT_2021_baseline.csv").sample(1000)
model = joblib.load("vultar_final_brain.pkl")

def check_for_drift(live_data_batch):
    """
    Compares live SCADA traffic to the original training distribution.
    If the 'Distance' is too high, the model is 'drifting'.
    """
    drift_detected = False
    for column in reference_data.columns:
        stat, p_value = ks_2samp(reference_data[column], live_data_batch[column])
        if p_value < 0.05: # Statistical significance of a shift
            print(f"⚠️ Drift detected in feature: {column}")
            drift_detected = True
            break
    return drift_detected

def trigger_retrain():
    print("🔄 Accuracy threshold breached. Triggering Automated Retrain...")
    # Execute the training script with the new augmented dataset
    subprocess.run(["python3", "7_final_train_with_smote.py"])
    # Notify the Admin (You)
    print("✅ New Brain 'v2' deployed to the Admission Controller.")

# Simulated Loop
while True:
    live_batch = pull_latest_ebpf_telemetry() # Pulls from Cilium/Hubble
    if check_for_drift(live_batch):
        trigger_retrain()