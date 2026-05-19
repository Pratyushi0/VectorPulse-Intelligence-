from flask import Flask, request, jsonify
import joblib
import pandas as pd
import datetime
import os

app = Flask(__name__)

# Load the trained model
model = joblib.load("sentinel_brain.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # 1. Convert incoming features to DataFrame
        features = data.get('features')
        df = pd.DataFrame([features], columns=model.feature_names_in_)
        
        # 2. AI Prediction
        prediction = int(model.predict(df)[0])
        status = "MALICIOUS" if prediction == 1 else "NORMAL"
        
        # 3. Log to CSV for the Dashboard
        log_file = "traffic_logs.csv"
        log_entry = pd.DataFrame([[datetime.datetime.now(), status, data.get('source', 'Quantum-Sim')]], 
                                 columns=['timestamp', 'status', 'source'])
        
        log_entry.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)
        
        print(f"[{datetime.datetime.now()}] Classified as: {status}")
        return jsonify({"status": status, "prediction": prediction})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Start on 8448 to avoid Mac system conflicts
    app.run(host='0.0.0.0', port=8448, ssl_context=('sentinel.crt', 'sentinel.key'))