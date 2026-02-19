# MoneyGuard 🛡️
### An ML-Powered Fraud & AML Detection System for Ghana's Mobile Money Ecosystem

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Regulation](https://img.shields.io/badge/Regulation-BoG%20Act%20987%20%7C%20Act%20749-red)

---

## The Problem

**Ghana's mobile money ecosystem processes over 1 billion transactions annually. Fraudsters are winning.**

Account takeover, OTP phishing, and structured fund draining are exploiting a critical gap: most fraud and AML detection systems in Ghanaian fintechs still run on static, rule-based engines with fixed thresholds. Sophisticated attackers know these thresholds. They stay below them.

The result is predictable:

- **Cross-channel attacks go undetected** — a compromised MoMo wallet becomes a launchpad into linked bank accounts, often days later, with no system-level correlation between the two events
- **Structured draining evades velocity checks** — repeated small transfers and withdrawals are designed to look like normal behavior to rule engines
- **Behavioral anomalies are invisible** — there is no baseline of *who the customer is*, so there is nothing to compare against when the attacker takes over

By the time a Suspicious Transaction Report reaches the Financial Intelligence Centre under **Act 749**, the money is gone.

**MoneyGuard** replaces reactive, rules-only monitoring with a hybrid ML system that detects anomalies in real time, correlates signals across channels, and generates explainable alerts that compliance officers can act on — and regulators can audit.

---

## Objectives

| # | Objective | Why It Matters |
|---|-----------|----------------|
| 1 | Reduce **false negative rates** in fraud detection across MoMo and linked bank transactions | Every missed fraud event is real money lost and regulatory exposure |
| 2 | Reduce **false positive rates** to minimize alert fatigue among compliance analysts | Analysts who see too many false alarms stop trusting the system |
| 3 | Detect **cross-channel attacks** by correlating MoMo and bank account signals in near real-time | The most damaging attacks exploit the monitoring gap between channels |
| 4 | Generate **human-readable explanations** for every alert via SHAP | Compliance officers must make defensible decisions without needing to understand the model |
| 5 | Demonstrate compliance with the **BoG Consumer Protection Directive 2022** through automated customer notification triggers | Customers have a right to be notified of suspicious activity on their accounts |
| 6 | Reduce **mean time to flag (MTTF)** for structured draining attacks from days to minutes | Speed of detection directly determines how much can be recovered |
| 7 | Provide a **risk-tiered alerting system** so analysts prioritize high-confidence flags first | Not all alerts are equal — analyst time should go to the highest-risk events |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA INGESTION LAYER                    │
│         MoMo Transactions  │  Bank Account Transactions     │
└────────────────┬────────────────────────┬───────────────────┘
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   FEATURE ENGINEERING                       │
│   Velocity Features │ Behavioral Baseline │ Channel Flags   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
┌───────────────────────┐    ┌─────────────────────────────┐
│  UNSUPERVISED LAYER   │    │     SUPERVISED LAYER        │
│   Isolation Forest    │    │   XGBoost / LightGBM        │
│  (Novel pattern det.) │    │  (Labelled attack patterns) │
└───────────┬───────────┘    └──────────────┬──────────────┘
            │                               │
            └──────────────┬────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│               CROSS-CHANNEL CORRELATION ENGINE              │
│     Links MoMo events → Bank events by account + time      │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXPLAINABILITY LAYER                      │
│              SHAP values → Human-readable rationale         │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  RISK-TIERED ALERT ENGINE                   │
│              HIGH 🔴  │  MEDIUM 🟡  │  LOW 🟢              │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT DASHBOARD                       │
│    Alert Queue │ Transaction Detail │ SHAP Waterfall Chart  │
└─────────────────────────────────────────────────────────────┘
```

---

## Attack Patterns Modeled

| Pattern | Description | Real-World Example |
|---------|-------------|-------------------|
| **OTP Phishing** | Attacker socially engineers victim into sharing MoMo authorization code | Fake Google Maps restaurant listing |
| **Account Takeover (ATO)** | Attacker uses shared credentials to access linked bank accounts | Same PIN across MoMo and bank |
| **Structured Draining** | Repeated below-threshold transfers to evade velocity checks | Multiple GHS 500 withdrawals instead of one GHS 5,000 |
| **Cross-Channel Lateral Movement** | MoMo compromise used as entry point to bank account days later | 48-hour delay between MoMo and bank attack |

---

## Regulatory Mapping

| Regulation | Jurisdiction | Relevance to GhanaGuard |
|------------|-------------|--------------------------|
| **Anti-Money Laundering Act, 2008 (Act 749)** | Ghana | STR filing obligations; defines suspicious transaction criteria |
| **AML (Amendment) Act, 2014 (Act 874)** | Ghana | Extends obligations to mobile money operators |
| **Payment Systems and Services Act, 2019 (Act 987)** | Ghana | Governs MoMo providers; mandates AML/CFT controls |
| **BoG Consumer Protection Directive, 2022** | Ghana | Customer notification obligations for suspicious account activity |
| **Data Protection Act, 2012 (Act 843)** | Ghana | Governs use of customer data in ML model training and inference |
| **FATF Recommendation 16** | International | Wire transfer rules; applies to MoMo cross-border transactions |
| **GIABA Mutual Evaluation Framework** | West Africa | Regional AML/CFT compliance context for Ghana |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Data Generation | Python, Faker |
| ML — Unsupervised | Scikit-learn (Isolation Forest) |
| ML — Supervised | XGBoost / LightGBM |
| Class Imbalance | imbalanced-learn (SMOTE) |
| Explainability | SHAP |
| Dashboard | Streamlit |
| Visualization | Plotly, Seaborn |
| Environment | Docker |

---

## Project Structure

```
ghanaGuard/
│
├── data/
│   ├── raw/              # Not committed — placeholder for real data
│   ├── processed/        # Feature-engineered datasets
│   └── synthetic/        # Generated MoMo + bank transaction data
│
├── notebooks/
│   ├── 01_eda.ipynb              # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb
│   ├── 03_anomaly_detection.ipynb
│   ├── 04_supervised_model.ipynb
│   ├── 05_cross_channel_correlation.ipynb
│   └── 06_explainability.ipynb
│
├── src/
│   ├── data/             # Synthetic data generation
│   ├── models/           # Model training and evaluation
│   ├── explainability/   # SHAP integration
│   ├── correlation/      # Cross-channel correlation engine
│   └── alerts/           # Risk tiering and alert generation
│
├── dashboard/            # Streamlit app
├── docs/                 # Regulatory brief, architecture docs
├── tests/                # Unit tests
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/ghanaGuard.git
cd ghanaGuard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate synthetic dataset
python src/data/generate_data.py

# Run the dashboard
streamlit run dashboard/app.py
```

---

## Results (MVP)

> Results will be populated as each module is completed.

| Metric | Baseline (Rules-Only) | GhanaGuard (ML Hybrid) |
|--------|----------------------|------------------------|
| False Negative Rate | TBD | TBD |
| False Positive Rate | TBD | TBD |
| Mean Time to Flag | Days | TBD |
| Cross-Channel Detection | ❌ | ✅ |
| Explainable Alerts | ❌ | ✅ |

---

## Future Work

- **Real-time streaming** via Apache Kafka or AWS Kinesis
- **REST API** via FastAPI for integration with core banking systems
- **Automated customer notification** pipeline (BoG CPD 2022 full compliance)
- **Model retraining pipeline** with drift detection
- **Network graph analysis** for mule account detection

---

## Author

**Efua Ahmed**
Specialising in secure, ethical fintech solutions.

---

## License

MIT License — see `LICENSE` for details.

---

> *This project uses synthetic data generated to model Ghana's mobile money ecosystem. No real customer data is used.*
