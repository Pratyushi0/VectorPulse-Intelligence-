import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# LOAD: Ensure you have downloaded WUSTL-IIoT-2021.csv
df = pd.read_csv("WUSTL_IIOT_2021.csv")

# PRE-PROCESS: Per dataset documentation, remove identifying metadata
# so the AI learns 'patterns', not just 'IP addresses'.
drop_cols = ['StartTime', 'LastTime', 'SrcAddr', 'DstAddr', 'sIpId', 'dIpId', 'Traffic']
X = df.drop(columns=drop_cols + ['target']) # 'target' is our label
y = df['target'] # 0 = Normal, 1 = Attack

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# TRAIN: Optimized for Industrial Anomaly Detection
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    tree_method='hist' # Faster training for large IoT datasets
)

model.fit(X_train, y_train)

# VERIFY: We are aiming for 99.9%
preds = model.predict(X_test)
print(f"🎯 Sentinel Accuracy: {accuracy_score(y_test, preds) * 100:.4f}%")

# SAVE: This model will be loaded by the K8s Operator
joblib.dump(model, "sentinel_brain.pkl")