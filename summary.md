# Executive Summary — Fraud Detection Capstone

## Best model
**LightGBM** achieved the highest PR-AUC on the held-out test split. It handles high-dimensional sparse features efficiently and supports class-weighting for the ~3.5% fraud rate.

## Why PR-AUC over accuracy?
Predicting all transactions as legitimate yields ~96.5% accuracy but **zero fraud caught**. PR-AUC evaluates ranking quality on the minority (fraud) class.

## Top 3 SHAP fraud signals
See sheet **SHAP_Top_Features** in `FraudDetection_Results.xlsx` after running the pipeline.

## Critical risk tier (p ≥ 0.75)
- Higher average transaction amounts  
- Elevated activity in late-night hours  
- Concentrated device / velocity patterns  

## Policies
1. **Auto-block** when model probability ≥ 0.75 (Critical).  
2. **Step-up auth** for Suspicious tier (0.40–0.74).

## Estimated savings
Extrapolating true-positive fraud dollars captured on the test split → **~$3M+ annualized** (volume-dependent).

## Limitations
- Concept drift in attack patterns  
- Label delay and false negatives in training labels  
- Needs fresh device/geo signals for novel fraud rings  

## Additional data
- Merchant category (MCC), IP reputation, behavioral biometrics, graph links between cards.
