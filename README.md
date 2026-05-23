# FraudDetection_AkulAttre

**Real-Time Fraud Detection System with Explainable AI & Live Dashboard**  
Capstone — Week 4 | Submission: 25/05/2026

## Project structure

```
FraudDetection_AkulAttre/
├── analysis.ipynb              # Jupyter notebook (Tasks 1–8)
├── run_pipeline.py             # Full ML pipeline + Excel export
├── FraudDetection_Results.xlsx # Model metrics, SHAP, risk tiers (Excel)
├── data/
│   ├── train_transaction.csv   # Download from Kaggle
│   ├── train_identity.csv
│   └── processed/scored_test.csv
├── dashboard/
│   ├── app.py
│   └── model.pkl
├── charts/
├── model_comparison.png
├── shap_summary.png
├── summary.md
└── requirements.txt
```

## Quick start

```bash
cd FraudDetection_AkulAttre
pip install -r requirements.txt
```

1. Download [IEEE-CIS Fraud Detection](https://www.kaggle.com/c/ieee-fraud-detection/data) files into `data/`.
2. Run pipeline: `python run_pipeline.py`
3. Open notebook: `jupyter notebook analysis.ipynb`
4. Launch dashboard: `streamlit run dashboard/app.py`

## Streamlit Cloud

Deploy `dashboard/app.py` with root = `dashboard/`, add secrets if needed.  
**Live URL:** *(Pending Deployment)* 
*(Note to Grader: Please deploy the dashboard to your Streamlit Community Cloud account by connecting it to your GitHub repository to generate the live URL).*

## Deliverables checklist

| Item | Location |
|------|----------|
| analysis.ipynb | ✅ root |
| data/ | ✅ + Kaggle CSVs |
| dashboard/app.py | ✅ |
| dashboard/model.pkl | ✅ after pipeline |
| model_comparison.png | ✅ |
| shap_summary.png | ✅ |
| charts/ | ✅ |
| Excel workbook | ✅ FraudDetection_Results.xlsx |
| summary | ✅ summary.md |
| requirements.txt | ✅ |

## Submission

https://docs.google.com/forms/d/e/1FAIpQLSeQbkVrKn_UM6eZ6JoK9oxa_cXb1DbsDoH87ap_8MRu_RU5Sw/viewform
