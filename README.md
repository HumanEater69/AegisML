# AegisML

**Real-Time Fraud Detection System with Explainable AI & Live Dashboard**

## Overview
AegisML is an enterprise-grade fraud detection engine built to identify anomalous financial transactions with high precision. By combining robust machine learning models (LightGBM, XGBoost, Isolation Forest) with SHAP-based Explainable AI (XAI), AegisML not only stops fraud in its tracks but provides clear, actionable reasoning for every blocked transaction.

## Key Features
- **High-Performance ML Pipeline**: Automated preprocessing, class balancing via SMOTE, and hyperparameter tuning utilizing Optuna.
- **Explainable AI (XAI)**: Native integration of SHAP values to explain feature importance globally and per-transaction.
- **Interactive Command Center**: A sleek, glassmorphic Streamlit dashboard for real-time monitoring, transaction lookup, and risk-tier visualization.
- **Comprehensive Reporting**: Automatically exports model metrics, SHAP top features, and business insights to an interactive Excel workbook.

## Project Structure
```text
AegisML/
├── analysis.ipynb              # Exploratory Data Analysis & Modeling Notebook
├── run_pipeline.py             # End-to-end ML pipeline & Excel export script
├── FraudDetection_Results.xlsx # Automated model insights and business metrics
├── data/                       # Directory for raw and processed datasets
├── dashboard/                  # Streamlit application components
│   ├── app.py                  # Main dashboard script
│   └── model.pkl               # Serialized ML model
├── charts/                     # Generated evaluation plots and SHAP waterfalls
└── requirements.txt            # Python dependencies
```

## Getting Started

### Prerequisites
- Python 3.9+
- The IEEE-CIS Fraud Detection dataset (download from Kaggle and place inside `data/`).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HumanEater69/AegisML.git
   cd AegisML
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. **Run the Pipeline**: Execute the full modeling pipeline to train the model and generate reports.
   ```bash
   python run_pipeline.py
   ```
2. **Launch the Dashboard**: Start the interactive command center.
   ```bash
   streamlit run dashboard/app.py
   ```

## Architecture
- **Models**: LightGBM (Primary), XGBoost, Isolation Forest
- **Data Processing**: Pandas, Scikit-learn
- **Visualization**: Matplotlib, Plotly, Seaborn, Streamlit
- **Explainability**: SHAP
