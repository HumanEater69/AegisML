# AegisML Folder and Dashboard Analysis

## 1. Overview of the Project Structure
The `AegisML` folder represents an enterprise-grade, end-to-end fraud detection platform tailored for high-velocity financial transactions. The system is split into multiple modules for data analysis, inference serving, and a highly stylized operational dashboard.

### Directory Tree Breakdown
- **`dashboard/`**: Contains the frontend Streamlit application (`app.py`), the logo (`aegisml_logo.png`), and the trained model (`model.pkl`).
- **`src/inference/`**: Houses the FastAPI backend (`main.py`) which acts as the real-time inference API for fraud predictions.
- **`notebooks/`**: Contains `analysis.py`, the core data pipeline script responsible for data preprocessing, training (LightGBM/XGBoost), and generating SHAP values.
- **`charts/`**: Stores generated visualizations (e.g., `shap_summary.png`, `roc_pr_curves.png`) created during the analysis phase.
- **`data/`**: Separated into `raw/` and `processed/` for structured data ingestion.
- **`design.md`**: Defines the UI/UX architecture, explicitly calling for "LIQUID GLASS + DEEP NEONISM + CLAYMORPHISM AT MAXIMUM INTENSITY" with specified color codes and typography (`Orbitron`, `Rajdhani`, `JetBrains Mono`).
- **`start_aegisml.bat`**: A multi-step Windows batch script that automates the installation of dependencies, launches the FastAPI backend on port 8080, and boots the Streamlit UI.
- **`README.md`**: Outlines the system architecture, business impact (projected $3M+ annual savings), and deployment instructions.

---

## 2. Deep Dive: The AegisML Dashboard (`dashboard/app.py`)

The Streamlit dashboard is a robust, 950+ line frontend built to resemble a high-security fintech "war room." It utilizes extensive raw HTML/CSS injection to override Streamlit's native styling, achieving a highly immersive "Cyberpunk" aesthetic.

### Key UI/UX Innovations
- **Cinematic Boot Sequence**: Uses CSS animations to simulate a neural lattice decryption and access-granted sequence upon initial load.
- **Native Sidebar Overridden**: The default Streamlit sidebar is hidden and replaced by a custom "iOS-style Bottom Dock" using a styled `st.radio` component to allow fluid navigation without page reloads.
- **Global CSS & Theming**: Employs animated glowing borders, `clay-card` divs with complex box-shadows, floating ambient orbs in the background, and neon typography.
- **Custom Plotly Theme Engine**: A centralized function (`apply_theme`) dynamically wraps all Plotly charts with cyberpunk styling (dark transparent backgrounds, JetBrains Mono tick fonts, and matching grid lines).

### Navigation & Views (The "Pages")
The dashboard is split into 4 core views:

#### 1. 📊 Overview
- Displays high-level KPIs (`TOTAL TXN`, `FRAUD DETECTED`, `CRITICAL ALERTS`).
- **Visualizations**: 
  - 3D Scatter and Surface plots detailing the Probability Space across Hours and Transaction Amounts.
  - Violin plots for Transaction Amount distribution.
  - Radar chart comparing `LightGBM`, `XGBoost`, and `Isolation Forest` model performance metrics.
  - Precision-Recall curves and cumulative fraud detection area charts.
- **Key Findings**: Presents automated insights like Fraud Rate, Peak Fraud Hour, and Average Fraud Amount in animated clay-styled cards.

#### 2. 🔎 Explorer
- A live transaction event log.
- Features a Risk Map (Hour vs. Amount Scattergl plot colored by risk tier).
- Displays ROC curves with an optimal threshold indicator.
- Contains a stylized, scrollable "Glass Table" of transactions, color-coded by Critical, Suspicious, or Clear risk tiers.

#### 3. 🧠 SHAP (Neural Explainer)
- Provides **Explainable AI (XAI)** capabilities.
- Users can input a `Transaction ID` to visualize precisely why a transaction was flagged.
- Features a dynamic waterfall chart showing feature contributions (e.g., `DeviceRisk`, `TransactionAmt`).
- Renders human-readable text blocks explaining how each factor raised or lowered the specific fraud risk.

#### 4. 🔮 Oracle (Live Simulator)
- A manual fraud injection form allowing the user to test the backend inference engine.
- Sends live payloads (via `requests.post`) to the FastAPI backend at `http://localhost:8080/api/v1/predict/quantum`.
- Outputs a detailed threat intelligence report including:
  - Dark Web Exposure, Botnet Signatures, Geo Velocity, and Biometric Trust.
- **LLM Simulation**: Simulates a typing effect of an AI "Oracle" providing contextual reasoning for the transaction's block, review, or allow status based on the risk tier.

---

## 3. System Orchestration

The system relies on the **`start_aegisml.bat`** script for local orchestration. The pipeline works as follows:
1. `pip install -r requirements.txt` (silently ensures dependencies).
2. Kills any lingering processes on port `8080`.
3. Spawns the `uvicorn` server for `src.inference.main` (The FastAPI Backend).
4. Delays for 4 seconds to ensure the API is listening.
5. Launches `streamlit run dashboard/app.py` (The Frontend).

## 4. Conclusion
The AegisML environment represents a highly polished, presentation-ready prototype. It successfully bridges hardcore machine learning pipelines (XGBoost/LightGBM, SHAP, Isotonic Calibration) with an exceptionally customized, premium frontend UI that breaks the boundaries of standard Streamlit applications.
