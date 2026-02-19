# MoneyGuard 🛡️
### An ML-Powered Fraud & AML Detection System for Ghana's Mobile Money Ecosystem

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Regulation](https://img.shields.io/badge/Regulation-BoG%20Act%20987%20%7C%20Act%20749-red)

---

## The Problem

**Ghana's mobile money ecosystem processed GHS 1.07 trillion in transactions in 2023. Fraudsters are taking an increasing share.**

The Bank of Ghana reported 13,451 fraud cases across the financial sector in 2023. Mobile money fraud accounted for approximately 20% of those cases, with total sector losses reaching GHS 56 million — up from GHS 33 million in 2021. More than GHS 10 million of those losses came directly from mobile money fraud.
Yet the systems meant to catch it are failing. Most fraud and AML detection in Ghanaian fintechs still runs on static, rule-based engines with fixed thresholds. Sophisticated attackers know these thresholds. They stay below them.
The result is predictable:

Cross-channel attacks go undetected — a compromised MoMo wallet becomes a launchpad into linked bank accounts, often days later, with no system-level correlation between the two events
Structured draining evades velocity checks — repeated small transfers and withdrawals are designed to look like normal behaviour to rule engines
Behavioral anomalies are invisible — there is no baseline of who the customer is, so there is nothing to compare against when the attacker takes over
Low-income users are most exposed — the GHS 10,000 reporting threshold offers no protection to the majority of MoMo users whose entire account balance sits below it

By the time a Suspicious Transaction Report reaches the Financial Intelligence Centre under Act 749, the money is gone.
**MoneyGuard** replaces reactive, rules-only monitoring with a hybrid ML system that detects anomalies in real time, correlates signals across channels, and generates explainable alerts that compliance officers can act on — and regulators can audit.
Built for Ghana's regulatory reality: BoG Act 987, Act 749/874, the Consumer Protection Directive 2022, and FATF Recommendation 16.

**Source: Bank of Ghana Annual Report 2023; MyJoyOnline — Mobile Payment Fraud in Ghana: A Growing Cybersecurity Challenge (August 2025)**

---

## Objectives

| # | Objective | Why It Matters |
|---|-----------|----------------|
| 1 | Reduce **false negative rates** in fraud detection across MoMo and linked bank transactions | Every missed fraud event is real money lost and real regulatory exposure |
| 2 | Reduce **false positive rates** to minimize alert fatigue among compliance analysts | Analysts who see too many false alarms stop trusting the system |
| 3 | Detect **cross-channel attacks** by correlating MoMo and bank account signals in near real-time | The most damaging attacks exploit the monitoring gap between channels |
| 4 | Generate **human-readable explanations** for every alert via SHAP | Compliance officers must make defensible decisions without needing to understand the model |
| 5 | Demonstrate compliance with the **BoG Consumer Protection Directive 2022** through automated customer notification triggers | Customers have a right to be notified of suspicious activity on their accounts |
| 6 | Reduce **mean time to flag (MTTF)** for structured draining attacks from days to minutes | Speed of detection directly determines how much can be recovered |
| 7 | Provide a **risk-tiered alerting system** so analysts prioritize high-confidence flags first | Not all alerts are equal — analyst time should go to the highest-risk events |

---

## Design Principle: Inclusive Fraud Detection

> **The BoG GHS 10,000 reporting threshold is a regulatory floor — not a fraud detection limit.**

Ghana's AML framework requires financial institutions to file Suspicious Transaction Reports (STRs) for transactions exceeding GHS 10,000. This threshold exists to catch large-scale money laundering. It was never designed to protect everyday Ghanaians.

Consider a farmer earning GHS 1,000 a month with GHS 300 remaining in her account. A fraudster draining GHS 280 in three rapid withdrawals will never trigger a GHS 10,000 rule engine. But it will wipe her out entirely.

**MoneyGuard uses behavioural baselining instead of fixed thresholds.** Every customer has a personal anomaly threshold derived from their own transaction history and income profile. A GHS 400 withdrawal at 2am from a low-income account is treated with the same scrutiny as a GHS 25,000 withdrawal from a corporate account — because both represent the same level of deviation from that customer's normal behaviour.

This approach:
- Protects low-income users, farmers, traders, and market women who sit far below the GHS 10,000 floor
- Aligns with **FATF's financial inclusion guidance**, which calls for proportionate, risk-based AML controls
- Supports **BoG's financial inclusion mandate** under the National Financial Inclusion and Development Strategy
- Does **not** conflict with Act 749 — it goes beyond it

MoneyGuard models Ghana's socioeconomic reality directly in the data: **55% of simulated customers are low-income**, reflecting the demographics of Ghana's MoMo user base.

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
│   Velocity Features │ Behavioural Baseline │ Channel Flags  │
│         Income Tier │ Personal Threshold   │ Time Patterns  │
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
| **Structured Draining** | Repeated below-personal-threshold transfers to evade velocity checks | Multiple withdrawals just under customer's behavioural limit |
| **Cross-Channel Lateral Movement** | MoMo compromise used as entry point to bank account days later | 24–72 hour delay between MoMo and bank attack |

---

## Regulatory Mapping

| Regulation | Jurisdiction | Relevance to MoneyGuard |
|------------|-------------|--------------------------|
| **Anti-Money Laundering Act, 2008 (Act 749)** | Ghana | STR filing obligations; defines suspicious transaction criteria |
| **AML (Amendment) Act, 2014 (Act 874)** | Ghana | Extends obligations to mobile money operators |
| **Payment Systems and Services Act, 2019 (Act 987)** | Ghana | Governs MoMo providers; mandates AML/CFT controls |
| **BoG Consumer Protection Directive, 2022** | Ghana | Customer notification obligations for suspicious account activity |
| **Data Protection Act, 2012 (Act 843)** | Ghana | Governs use of customer data in ML model training and inference |
| **FATF Recommendation 16** | International | Wire transfer rules; applies to MoMo cross-border transactions |
| **FATF Financial Inclusion Guidance** | International | Supports proportionate, risk-based controls that protect all income levels |
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
| Environment | Docker (planned) |

---

## Project Structure

```
MoneyGuard/
│
├── data/
│   ├── raw/              # Not committed — placeholder for real data
│   ├── processed/        # Feature-engineered datasets
│   └── synthetic/        # Generated MoMo + bank transaction data
│
├── notebooks/
│   ├── 01_eda.ipynb
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
git clone https://github.com/miss-nana/MoneyguardGH.git
cd MoneyguardGH

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux

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

| Metric | Baseline (Rules-Only) | MoneyGuard (ML Hybrid) |
|--------|----------------------|------------------------|
| False Negative Rate | TBD | TBD |
| False Positive Rate | TBD | TBD |
| Mean Time to Flag | Days | TBD |
| Cross-Channel Detection | ❌ | ✅ |
| Explainable Alerts | ❌ | ✅ |
| Low-Income User Protection | ❌ | ✅ |

---

## Future Work

- **Real-time streaming** via Apache Kafka or AWS Kinesis
- **REST API** via FastAPI for integration with core banking systems
- **Automated customer notification** pipeline (BoG CPD 2022 full compliance)
- **Model retraining pipeline** with drift detection
- **Network graph analysis** for mule account detection
- **SMS alert integration** with MTN, Vodafone Cash, and AirtelTigo Money APIs

---

## Author

**[Your Name]**
MSc IT for Business | Data Scientist | Business Strategist
Specialising in secure, ethical, and inclusive fintech solutions.

[LinkedIn](#) · [GitHub](https://github.com/miss-nana/MoneyguardGH)

---

## License

MIT License — see `LICENSE` for details.

---

> *This project uses synthetic data generated to model Ghana's mobile money ecosystem. No real customer data is used.*
