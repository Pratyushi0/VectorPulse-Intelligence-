# VectorPulse Intelligence

**AI-driven threat detection and autonomous incident response — built for Kubernetes, hardened with Post-Quantum Cryptography.**

VectorPulse is a security mesh that runs inside your cluster. It trains on real IIoT traffic, classifies threats in real time via a Flask inference API, and triggers self-healing responses without human intervention. The cryptographic layer uses ML-DSA (CRYSTALS-Dilithium) to sign workloads and rotate secrets, protecting against harvest-now-decrypt-later attacks before quantum hardware makes that threat real.

---

## What it does

The system has four layers that work together:

**1. Training (`3_train_sentinel.py`, `7_final_train_with_smote.py`)**  
Trains an XGBoost classifier on the WUSTL-IIoT-2021 dataset — industrial network traffic with labeled attack patterns. SMOTE balances the training set so the model doesn't just memorize the majority class. The trained model gets serialized to `sentinel_brain.pkl`.

**2. Inference API (`Security_brain.py`)**  
A Flask server that loads the trained model and exposes a `/predict` endpoint over HTTPS. Each request gets classified as `NORMAL` or `MALICIOUS`, logged to `traffic_logs.csv`, and returned with a confidence label. Runs on port 8448 with TLS.

**3. Kubernetes Operator (`k8s_operator.py`, `hardened_operator.py`, `4_self_healing_operator.py`)**  
A custom K8s operator watches the inference logs and reacts. Malicious traffic triggers automatic workload quarantine and secret rotation without downtime. The admission webhook (`6_admission_webhook.py`) intercepts pod creation and rejects workloads that haven't been signed with the PQC identity.

**4. Post-Quantum Cryptographic Layer (`2_generate_pqc_identity.py`, `generate_keys.py`, `5_sign_image.sh`)**  
Generates ML-DSA keypairs via liboqs and signs container images before deployment. The Kubernetes operator verifies signatures on admission. If a secret needs rotating, it happens automatically — the operator handles the full key lifecycle.

---

## Architecture

```
Traffic / Attacker Simulation
        │
        ▼
  Flask Inference API  ──► traffic_logs.csv
  (Security_brain.py)         │
        │                     ▼
        │              Dashboard (9_final_dashboard.py)
        ▼
  Self-Healing Operator
  (hardened_operator.py)
        │
        ├──► Quarantine malicious workloads
        ├──► Rotate PQC secrets (ML-DSA)
        └──► Admission Webhook blocks unsigned pods
```

---

## File Reference

| File | What it does |
|------|-------------|
| `3_train_sentinel.py` | Train XGBoost model on WUSTL-IIoT-2021 |
| `7_final_train_with_smote.py` | Retrain with SMOTE for class balancing |
| `Security_brain.py` | Flask HTTPS inference API |
| `sentinel_brain.pkl` | Serialized trained model |
| `k8s_operator.py` | Base Kubernetes operator |
| `hardened_operator.py` | Hardened operator with PQC integration |
| `4_self_healing_operator.py` | Auto-quarantine + key rotation logic |
| `6_admission_webhook.py` | Webhook to block unsigned workloads |
| `2_generate_pqc_identity.py` | Generate ML-DSA keypair via liboqs |
| `generate_keys.py` | Key generation utilities |
| `5_sign_image.sh` | Sign container images with PQC key |
| `consensus_engine.py` | Multi-node consensus for threat decisions |
| `quorum_voter.py` | Quorum voting logic |
| `audit_exporter.py` | Export audit logs |
| `deffence_line.py` | Defense perimeter logic |
| `handshake.py` | Mutual TLS handshake utilities |
| `9_final_dashboard.py` | Real-time threat dashboard |
| `attacker.py` | Attack traffic simulator for testing |
| `sentinel-cluster.yaml` | Kubernetes cluster manifest |
| `traffic_logs.csv` | Live inference log |

---

## Setup

### Prerequisites

- Python 3.9+
- Kubernetes cluster (local: `kind` or `minikube`)
- liboqs installed (see `liboqs` in repo root)
- WUSTL-IIoT-2021 dataset ([download here](https://www.cse.wustl.edu/~jain/iiot2/index.html))

### 1. Install dependencies

```bash
pip install xgboost scikit-learn imbalanced-learn pandas joblib flask kubernetes
```

### 2. Train the model

```bash
# Place WUSTL_IIOT_2021.csv in the repo root, then:
python 3_train_sentinel.py

# Optional: retrain with SMOTE for better class balance
python 7_final_train_with_smote.py
```

### 3. Generate PQC identity

```bash
python 2_generate_pqc_identity.py
python generate_keys.py
```

### 4. Sign your container image

```bash
bash 5_sign_image.sh <your-image>
```

### 5. Deploy to Kubernetes

```bash
bash setup_cluster.sh
kubectl apply -f sentinel-cluster.yaml
```

### 6. Start the inference API

```bash
python Security_brain.py
# Listening on https://0.0.0.0:8448
```

### 7. Run the dashboard

```bash
python 9_final_dashboard.py
```

---

## Running the attacker simulation

To test detection without real malicious traffic:

```bash
python attacker.py
```

This sends crafted packets to the inference API and verifies they get classified as `MALICIOUS` and trigger the self-healing loop.

---

## Dataset

This project trains on **WUSTL-IIoT-2021**, a labeled industrial IoT network traffic dataset from Washington University in St. Louis. It covers normal traffic and 7 attack categories including DoS, reconnaissance, and backdoor patterns.

The model drops identifying metadata (IP addresses, timestamps) before training so it learns behavioral patterns, not endpoint identifiers.

---

## Tech Stack

`Python` · `XGBoost` · `Flask` · `Kubernetes` · `liboqs (ML-DSA)` · `SMOTE` · `Pandas` · `scikit-learn` · `Docker` · `Bash`

---

## Status

Active development. Core detection and self-healing loop are functional. PQC admission control is in hardening phase.

---

## Author

**Pratyush Sharma** — Cybersecurity Researcher & ML Engineer  
[LinkedIn](https://linkedin.com) · [Portfolio / GitHub](https://github.com/Pratyushi0)
