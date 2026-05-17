# AegisML — Real-Time Fraud Detection System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

AegisML is an enterprise-grade, end-to-end fraud detection platform engineered to process high-velocity financial transactions. It identifies anomalies and malicious activities in real-time, leveraging the IEEE-CIS Fraud Detection dataset. 

## Executive Summary
This system goes beyond traditional binary classification by integrating advanced feature engineering, probability calibration, risk segmentation, and deep Explainable AI (SHAP). Designed for a fintech production environment, AegisML balances recall and precision to minimize financial losses while reducing false-positive friction for legitimate customers. 

## System Architecture

```text
[ Data Sources ]
      │
      ├──> Batch Data (S3/GCS)
      └──> Streaming Events (Kafka)
               │
               ▼
  [ Real-Time Inference API ] <────────────── [ ML Training Pipeline ]
    (FastAPI + Docker)                        - Missing Value Handling
      - Payload Validation                    - Feature Engineering
      - Online Feature Fetch                  - Target Encoding & Scaling
      - Model Scoring                         - SMOTE Imbalance Handling
      - Rule Engine Override                  - LightGBM / XGBoost
               │                                       │
               ▼                                       ▼
[ Explainability & Risk Layer ]              [ Model Registry (MLflow) ]
  - SHAP TreeExplainer
  - Probability Calibration (Isotonic)
  - Risk Tiers (Critical/Suspicious/Clear)
               │
               ▼
     [ Decision Output ] ─────────────────> [ Monitoring & Retraining ]
      (Block / Review / Allow)               - Data & Concept Drift
               │
               ▼
[ Risk Ops Dashboard (Streamlit) ]
  - KPI Overview & Financial Impact
  - Transaction Explorer
  - SHAP Global & Local Explainability
  - Threshold Simulator
```

## Setup & Quickstart

1. **Clone the repository** and navigate to the project root.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download Data**: Place `train_transaction.csv` and `train_identity.csv` in `data/raw/`.
4. **Run the Analysis Notebook**: Execute `notebooks/analysis.ipynb` to run the ML pipeline and generate models/charts.
5. **Launch the Dashboard**:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

## Business Impact
On the test set, the optimal LightGBM model achieves substantial cost savings:
- **Projected Savings**: ~$504K on the test split.
- **Annualized Savings**: Over $3M per year across the full transaction volume.
- **Precision vs Recall**: Optimized to flag the top ~5% of transactions representing the highest risk.

## Explainable AI (XAI)
AegisML integrates SHAP (SHapley Additive exPlanations) to provide local and global interpretability. Operations analysts can view exactly why a transaction was flagged in the Streamlit dashboard via plain-English narrations and waterfall plots.

## Deployment (API)
AegisML includes a FastAPI service for sub-100ms real-time inference.
```bash
cd src/inference
uvicorn main:app --reload
```
API Documentation available at `http://localhost:8000/docs`.
