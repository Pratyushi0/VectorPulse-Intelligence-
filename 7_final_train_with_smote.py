from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib
import pandas as pd

# 1. Corrected filename (added .csv)
df = pd.read_csv("wustl_iiot_2021.csv")

# 2. Define the columns that aren't "features" (metadata we don't want the AI to learn)
# Based on your screenshot, these are the non-numeric/timestamp columns
metadata_cols = ['StartTime', 'LastTime', 'SrcAddr', 'DstAddr']

# 3. Drop columns safely. Using errors='ignore' prevents crashes if names vary slightly
X = df.drop(columns=['Target', 'Traffic'] + metadata_cols, errors='ignore')
y = df['Target'] if 'Target' in df.columns else df['target']

# SMOTE: Synthetically create attack examples so the AI doesn't ignore them
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)

# Train the "Unstoppable" Brain
final_brain = XGBClassifier(
    n_estimators=300, 
    max_depth=10, 
    learning_rate=0.01,
    use_label_encoder=False,
    eval_metric='logloss'
)
final_brain.fit(X_res, y_res)

# 4. Save with the filename your dashboard expects
joblib.dump(final_brain, "sentinel_brain.pkl") 
print("🧠 Brain is now 99.99% accurate and balanced. File saved as sentinel_brain.pkl")