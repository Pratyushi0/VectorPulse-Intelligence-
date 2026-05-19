import requests
import time        
import random
import numpy as np
import joblib

# Load model just to get the feature names
model = joblib.load("sentinel_brain.pkl")
url = "https://localhost:8448/predict"

def send_packet(is_attack=False):
    # Generate random features matching the model's structure
    features = list(np.random.rand(len(model.feature_names_in_)))
    
    # If it's an attack, simulate high flow or specific ports (dummy logic)
    if is_attack:
        print("🚨 Sending MALICIOUS Quantum-Tunneling Payload...")
    else:
        print("✅ Sending Normal Telemetry...")

    payload = {
        "features": features,
        "source": "192.168.1.50" if not is_attack else "EXTERNAL_ATTACKER"
    }
    
    try:
        requests.post(url, json=payload, verify=False) # verify=False for self-signed certs
    except Exception as e:
        print(f"Connection Error: {e}")

while True:
    # 20% chance of an attack
    attack_mode = random.random() < 0.2
    send_packet(is_attack=attack_mode)
    time.sleep(2)