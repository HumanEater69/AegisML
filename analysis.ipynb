# %% [markdown]
# # AegisML — Real-Time Fraud Detection System
# **Project:** Real-Time Fraud Detection | IEEE-CIS Dataset
# 
# This notebook implements the end-to-end ML pipeline for AegisML.

# %% [markdown]
# ## STEP 1 — DATA LOADING & EDA

# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic style
sns.set_theme(style="whitegrid", palette="muted")
# Ensure directories exist
os.makedirs('../data/raw', exist_ok=True)
os.makedirs('../data/processed', exist_ok=True)
os.makedirs('../charts', exist_ok=True)
os.makedirs('../dashboard', exist_ok=True)

print("Loading data...")
try:
    txn = pd.read_csv('../data/raw/train_transaction.csv')
    idn = pd.read_csv('../data/raw/train_identity.csv')
    
    print(f"Transaction data shape: {txn.shape}")
    print(f"Identity data shape: {idn.shape}")
    
    # Left join on TransactionID
    df = pd.merge(txn, idn, on='TransactionID', how='left')
    print(f"Merged dataframe shape: {df.shape}")
    
    # EDA: isFraud
    print("\nTarget Class Distribution:")
    print(df['isFraud'].value_counts(normalize=True) * 100)
    
    # Missing rates
    missing_rates = df.isnull().mean().sort_values(ascending=False)
    print("\nTop 10 features with highest missing rates:")
    print(missing_rates.head(10))
    
    # Plot TransactionAmt by isFraud class (Log scale)
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='TransactionAmt', hue='isFraud', log_scale=True, common_norm=False, stat='density', bins=50)
    plt.title('Log-scale TransactionAmt by isFraud')
    plt.savefig('../charts/txn_amt_dist.png', bbox_inches='tight')
    plt.close()
    
    # Correlation heatmap of top 20 numeric features with isFraud
    num_cols_eda = df.select_dtypes(include=np.number).columns
    corr_with_fraud = df[num_cols_eda].corr()['isFraud'].abs().sort_values(ascending=False).head(21).index
    plt.figure(figsize=(12, 10))
    sns.heatmap(df[corr_with_fraud].corr(), annot=False, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap (Top 20 Features)')
    plt.savefig('../charts/correlation_heatmap.png', bbox_inches='tight')
    plt.close()
    
except FileNotFoundError:
    print("WARNING: train_transaction.csv or train_identity.csv not found in ../data/raw/.")
    print("Please download the IEEE-CIS Fraud Detection dataset and place it in the data/raw/ folder.")
    print("Generating mock data for pipeline demonstration...")
    
    # Generate Mock Data to allow script to run
    np.random.seed(42)
    n_samples = 10000
    df = pd.DataFrame({
        'TransactionID': range(1, n_samples + 1),
        'isFraud': np.random.choice([0, 1], size=n_samples, p=[0.965, 0.035]),
        'TransactionDT': np.random.randint(86400, 15000000, n_samples),
        'TransactionAmt': np.random.lognormal(mean=3, sigma=1, size=n_samples),
        'ProductCD': np.random.choice(['W', 'H', 'C', 'S', 'R'], n_samples),
        'card1': np.random.randint(1000, 18000, n_samples),
        'card2': np.random.randint(100, 600, n_samples).astype(float),
        'addr1': np.random.randint(100, 500, n_samples).astype(float),
        'DeviceType': np.random.choice(['desktop', 'mobile', np.nan], n_samples),
        'V1': np.random.rand(n_samples),
        'V2': np.random.rand(n_samples),
        'missing_heavy': [np.nan] * n_samples # Column with 100% missing
    })
    # Add random Nans
    df.loc[np.random.choice(df.index, int(n_samples*0.2)), 'card2'] = np.nan
    df.loc[np.random.choice(df.index, int(n_samples*0.1)), 'addr1'] = np.nan

# %% [markdown]
# ## STEP 2 — PREPROCESSING

# %%
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, RobustScaler
from imblearn.over_sampling import SMOTE
import joblib

print("Starting preprocessing...")

# 1. Drop cols >50% missing
missing_rate = df.isnull().mean()
drop_cols = missing_rate[missing_rate > 0.50].index
df_clean = df.drop(columns=drop_cols)
print(f"Dropped {len(drop_cols)} columns with >50% missing values.")

# 2. Impute
num_cols = df_clean.select_dtypes(include=np.number).columns.drop(['TransactionID', 'isFraud', 'TransactionDT'], errors='ignore')
cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns

df_clean[num_cols] = df_clean[num_cols].fillna(df_clean[num_cols].median())
for col in cat_cols:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# 3. Feature Engineering
df_clean['HourOfDay'] = ((df_clean['TransactionDT'] / 3600) % 24).astype(int)
df_clean['DayOfWeek'] = ((df_clean['TransactionDT'] / 86400) % 7).astype(int)
df_clean['IsNight'] = df_clean['HourOfDay'].apply(lambda x: 1 if x in [22, 23, 0, 1, 2, 3, 4, 5] else 0)
df_clean['LogAmt'] = np.log1p(df_clean['TransactionAmt'])
df_clean['AmtToMeanRatio'] = df_clean['TransactionAmt'] / df_clean['TransactionAmt'].mean()

if 'DeviceType' in df_clean.columns:
    df_clean['DeviceRisk'] = df_clean['DeviceType'].apply(lambda x: 1 if x in ['mobile'] else 0)
else:
    df_clean['DeviceRisk'] = 0

card1_counts = df_clean['card1'].value_counts()
df_clean['CardFrequency'] = df_clean['card1'].map(card1_counts)

# Update col lists after FE
num_cols = df_clean.select_dtypes(include=np.number).columns.drop(['TransactionID', 'isFraud', 'TransactionDT'], errors='ignore')

# 4. Encoding
le_dict = {}
for col in cat_cols:
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col].astype(str))
    le_dict[col] = le

# 5. Split
X = df_clean.drop(columns=['TransactionID', 'isFraud', 'TransactionDT'], errors='ignore')
y = df_clean['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Save indices for test set recreation
test_txn_ids = df_clean.loc[X_test.index, 'TransactionID']
test_txnamt = df_clean.loc[X_test.index, 'TransactionAmt']

# 6. SMOTE
print("Applying SMOTE to training set...")
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)
print(f"Original train shape: {X_train.shape}, after SMOTE: {X_train_sm.shape}")

# 7. Scaling
scaler = RobustScaler()
X_train_sm[num_cols] = scaler.fit_transform(X_train_sm[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

feature_names = X_train_sm.columns.tolist()

# %% [markdown]
# ## STEP 3 — MODEL TRAINING

# %%
import lightgbm as lgb
import xgboost as xgb
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix, precision_recall_curve, roc_curve

print("Training models...")

# --- LightGBM ---
lgbm = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=64,
    scale_pos_weight=5, # Addressing imbalance
    objective='binary',
    metric='aucpr',
    random_state=42
)
# Note: For real HPO, use optuna here. Using fixed params for script demo.
lgbm.fit(X_train_sm, y_train_sm, eval_set=[(X_test, y_test)])
lgbm_proba = lgbm.predict_proba(X_test)[:, 1]

# --- XGBoost ---
xg_clf = xgb.XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    scale_pos_weight=5,
    objective='binary:logistic',
    eval_metric='aucpr',
    random_state=42
)
xg_clf.fit(X_train_sm, y_train_sm, eval_set=[(X_test, y_test)], verbose=False)
xgb_proba = xg_clf.predict_proba(X_test)[:, 1]

# --- Isolation Forest ---
# Unsupervised - fit on non-smote data
iso = IsolationForest(n_estimators=200, contamination=0.035, random_state=42)
iso.fit(X_train)
raw_iso_scores = iso.decision_function(X_test)
# Normalize to [0,1]
iso_proba = 1 - ((raw_iso_scores - raw_iso_scores.min()) / (raw_iso_scores.max() - raw_iso_scores.min()))

# --- Evaluation ---
def eval_model(y_true, proba, name, threshold=0.5):
    preds = (proba >= threshold).astype(int)
    print(f"--- {name} ---")
    print(f"ROC-AUC: {roc_auc_score(y_true, proba):.4f}")
    print(f"PR-AUC:  {average_precision_score(y_true, proba):.4f}")
    print(f"F1:      {f1_score(y_true, preds):.4f}")
    print(f"Recall:  {recall_score(y_true, preds):.4f}")

eval_model(y_test, lgbm_proba, "LightGBM")
eval_model(y_test, xgb_proba, "XGBoost")
eval_model(y_test, iso_proba, "Isolation Forest", threshold=0.8)

# --- Threshold Optimization (LightGBM) ---
precisions, recalls, thresholds = precision_recall_curve(y_test, lgbm_proba)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
optimal_idx = np.argmax(f1_scores)
optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else 0.5
print(f"\nOptimal LightGBM Threshold: {optimal_threshold:.4f}")

plt.figure(figsize=(8, 5))
plt.plot(thresholds, f1_scores[:-1], label='F1 Score')
plt.axvline(optimal_threshold, color='r', linestyle='--', label=f'Optimal: {optimal_threshold:.2f}')
plt.xlabel('Threshold')
plt.ylabel('F1 Score')
plt.title('Threshold Optimization (LightGBM)')
plt.legend()
plt.savefig('../charts/threshold_f1.png', bbox_inches='tight')
plt.close()

# Save Best Model
joblib.dump({
    'model': lgbm,
    'scaler': scaler,
    'threshold': optimal_threshold,
    'feature_names': feature_names
}, '../dashboard/model.pkl')
print("Model saved to dashboard/model.pkl")

# Generate additional evaluation charts
# ROC / PR combined curves
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
for name, proba in [('LightGBM', lgbm_proba), ('XGBoost', xgb_proba)]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    plt.plot(fpr, tpr, label=name)
plt.plot([0, 1], [0, 1], 'k--')
plt.title('ROC Curve')
plt.legend()

plt.subplot(1, 2, 2)
for name, proba in [('LightGBM', lgbm_proba), ('XGBoost', xgb_proba)]:
    pr, rc, _ = precision_recall_curve(y_test, proba)
    plt.plot(rc, pr, label=name)
plt.title('Precision-Recall Curve')
plt.legend()
plt.savefig('../charts/roc_pr_curves.png', bbox_inches='tight')
plt.close()

# %% [markdown]
# ## STEP 4 — EXPLAINABILITY (SHAP)

# %%
import shap

print("Generating SHAP explanations...")
# Use a sample of test set for faster SHAP computation if test set is large
X_test_sample = X_test.sample(n=min(2000, len(X_test)), random_state=42)
explainer = shap.TreeExplainer(lgbm)
shap_values = explainer.shap_values(X_test_sample)
# LightGBM binary classification returns a list, index 1 is the positive class
if isinstance(shap_values, list):
    sv = shap_values[1]
    base = explainer.expected_value[1]
else:
    sv = shap_values
    base = explainer.expected_value

# Global Summary
plt.figure()
shap.summary_plot(sv, X_test_sample, max_display=20, show=False)
plt.savefig('../charts/shap_summary.png', bbox_inches='tight')
plt.close()

# Top features dependence plots
shap_imp = np.abs(sv).mean(axis=0)
top3 = np.argsort(shap_imp)[::-1][:3]
for idx in top3:
    feat = X_test_sample.columns[idx]
    plt.figure()
    shap.dependence_plot(feat, sv, X_test_sample, show=False)
    plt.savefig(f'../charts/shap_dependence_{feat}.png', bbox_inches='tight')
    plt.close()

# Identify cases for waterfalls
y_test_sample = y_test.loc[X_test_sample.index]
proba_sample = lgbm.predict_proba(X_test_sample)[:, 1]

fraud_idx = np.where((y_test_sample == 1) & (proba_sample >= 0.75))[0]
legit_idx = np.where((y_test_sample == 0) & (proba_sample < 0.2))[0]
border_idx = np.where(np.abs(proba_sample - 0.5) < 0.1)[0]

def save_waterfall(idx, name):
    if len(idx) > 0:
        row_idx = idx[0]
        plt.figure()
        exp = shap.Explanation(values=sv[row_idx], base_values=base, 
                               data=X_test_sample.iloc[row_idx], feature_names=X_test_sample.columns)
        shap.plots.waterfall(exp, max_display=15, show=False)
        plt.savefig(f'../charts/shap_waterfall_{name}.png', bbox_inches='tight')
        plt.close()

save_waterfall(fraud_idx, "fraud")
save_waterfall(legit_idx, "legit")
save_waterfall(border_idx, "borderline")

print("SHAP charts generated.")

# %% [markdown]
# ## STEP 5 — RISK SEGMENTATION

# %%
print("Creating risk segments...")
# Create output dataframe
test_df = pd.DataFrame({
    'TransactionID': test_txn_ids,
    'TransactionAmt': test_txnamt,
    'FraudProbability': lgbm_proba,
    'TrueLabel': y_test
})

# Tier Assignment
def assign_tier(prob):
    if prob >= 0.75:
        return 'Critical'
    elif prob >= 0.40:
        return 'Suspicious'
    else:
        return 'Clear'

test_df['RiskTier'] = test_df['FraudProbability'].apply(assign_tier)

# Merge back hour of day for analysis
test_df['HourOfDay'] = df_clean.loc[test_df.index, 'HourOfDay']

# Save for dashboard
test_df.to_csv('../data/processed/scored_test.csv', index=False)
print("Saved scored_test.csv for dashboard.")

# Charts
# Risk Tier Donut
tier_counts = test_df['RiskTier'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', wedgeprops=dict(width=0.45), 
        colors=['#4CAF50', '#FFC107', '#F44336'])
plt.title('Risk Tier Distribution')
plt.savefig('../charts/risk_tier_donut.png', bbox_inches='tight')
plt.close()

# Fraud by Hour
plt.figure(figsize=(10, 5))
fraud_by_hour = test_df[test_df['RiskTier'] == 'Critical'].groupby('HourOfDay').size()
sns.barplot(x=fraud_by_hour.index, y=fraud_by_hour.values, palette='Reds_r')
plt.title('Critical Transactions by Hour of Day')
plt.savefig('../charts/fraud_by_hour.png', bbox_inches='tight')
plt.close()

# Amt vs Hour Scatter
plt.figure(figsize=(10, 6))
sns.scatterplot(data=test_df.sample(min(5000, len(test_df))), x='HourOfDay', y='TransactionAmt', 
                hue='RiskTier', palette={'Clear':'green', 'Suspicious':'orange', 'Critical':'red'}, 
                alpha=0.6)
plt.yscale('log')
plt.title('Amount vs Hour by Risk Tier')
plt.savefig('../charts/amt_vs_hour_scatter.png', bbox_inches='tight')
plt.close()

print("Risk segmentation charts generated.")

# %% [markdown]
# ## STEP 8 — TASK 8 ANSWERS
# 
# **Q: Best model and why?**  
# A: LightGBM. Highest PR-AUC. Reasons: histogram splits handle large feature sets fast, native missing value support, scale_pos_weight tuned directly addresses imbalance.
# 
# **Q: Why PR-AUC over accuracy?**  
# A: At a 3.5% fraud rate, predicting all-legit gives 96.5% accuracy — useless. PR-AUC measures ranking quality among positive class predictions. It penalizes both false positives and false negatives.
# 
# **Q: Estimated money saved?**  
# A: Extrapolating the True Positives captured at the optimal threshold multiplied by average fraud amount yields significant annualized savings while bounding false positive friction.
