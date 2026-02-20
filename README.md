# MoneyGuard 🛡️
### An ML-Powered Fraud & AML Detection System for Ghana's Mobile Money Ecosystem

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Regulation](https://img.shields.io/badge/Regulation-BoG%20Act%20987%20%7C%20Act%20749-red)

> *This is an independent personal portfolio project built on synthetic data. MoneyGuard has no affiliation with the Bank of Ghana or any financial institution.*

---

## The Problem

**Ghana's mobile money ecosystem processed GHS 1.07 trillion in transactions in 2023. Fraudsters are taking an increasing share.**

The Bank of Ghana reported 13,451 fraud cases across the financial sector in 2023. Mobile money fraud accounted for approximately 20% of those cases, with total sector losses reaching GHS 56 million — up from GHS 33 million in 2021. More than GHS 10 million of those losses came directly from mobile money fraud.

Yet the systems meant to catch it are failing. Most fraud and AML detection in Ghanaian fintechs still runs on static, rule-based engines with fixed thresholds. Sophisticated attackers know these thresholds. They stay below them.

The result is predictable:

- **Cross-channel attacks go undetected** — a compromised MoMo wallet becomes a launchpad into linked bank accounts, often days later, with no system-level correlation between the two events
- **Structured draining evades velocity checks** — repeated small transfers and withdrawals are designed to look like normal behaviour to rule engines
- **Behavioral anomalies are invisible** — there is no baseline of *who the customer is*, so there is nothing to compare against when the attacker takes over
- **Low-income users are most exposed** — the GHS 10,000 reporting threshold offers no protection to the majority of MoMo users whose entire account balance sits below it
- **Weekend and holiday windows are exploited** — bank customer service is unavailable, victims cannot respond quickly, and attackers have maximum time before intervention

By the time a Suspicious Transaction Report reaches the Financial Intelligence Centre under **Act 749**, the money is gone.

**MoneyGuard** replaces reactive, rules-only monitoring with a hybrid ML system that detects anomalies in real time, correlates signals across channels, and generates explainable alerts that compliance officers can act on — and regulators can audit.

Built for Ghana's regulatory reality: **BoG Act 987, Act 749/874, the Consumer Protection Directive 2022, and FATF Recommendation 16.**

> *Sources: Bank of Ghana 2023 Annual Fraud Report; MyJoyOnline — Mobile Payment Fraud in Ghana: A Growing Cybersecurity Challenge (August 2025)*

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

The Bank of Ghana's own data shows the average MoMo transaction in 2023 was just GHS 281. A fixed GHS 10,000 threshold protects almost nobody.

**MoneyGuard uses behavioural baselining instead of fixed thresholds.** Every customer has a personal anomaly threshold derived from their own transaction history and income profile. A GHS 400 withdrawal at 2am from a low-income account is treated with the same scrutiny as a GHS 25,000 withdrawal from a corporate account — because both represent the same level of deviation from that customer's normal behaviour.

This approach:
- Protects low-income users, farmers, traders, and market women who sit far below the GHS 10,000 floor
- Aligns with **FATF's financial inclusion guidance**, which calls for proportionate, risk-based AML controls
- Supports **BoG's financial inclusion mandate** under the National Financial Inclusion and Development Strategy
- Does **not** conflict with Act 749 — it goes beyond it

MoneyGuard models Ghana's socioeconomic reality directly in the data across three income tiers — low, middle, and high — reflecting the demographics of Ghana's MoMo user base.

> *Source: Bank of Ghana 2024 Payment Systems Oversight Annual Report — average MoMo transaction value GHS 281 (2023), GHS 372 (2024)*

---

## Design Principle: Step-Up Authentication

> **A detection system that alerts after the fact is not enough. MoneyGuard recommends blocking high-risk transactions pending customer confirmation.**

A critical real-world gap MoneyGuard is designed to address: bank customer service is unavailable or severely limited on weekends and public holidays. Attackers exploit this window deliberately — a victim who notices fraud at 6pm on a Sunday cannot reach their bank for hours. By Monday morning, the account is empty.

MoneyGuard addresses this through risk-tiered step-up authentication triggers:

| Risk Score | Authentication Required |
|------------|------------------------|
| Low | PIN only |
| Medium | PIN + SMS OTP |
| High | PIN + SMS + Email confirmation |
| Critical | Transaction blocked pending manual review |

When a transaction deviates significantly from a customer's behavioural baseline AND occurs outside their normal time patterns, MoneyGuard flags it for step-up authentication **before** the transaction is approved — not after.

This directly addresses the BoG Consumer Protection Directive 2022 requirement for customer notification of suspicious activity, and goes further by making notification a prerequisite for transaction approval.

**Important design note for low digital literacy contexts:**
Step-up authentication prompts should be simple, unambiguous, and available in local languages. MoneyGuard's prompts are designed to never ask users to share codes verbally — directly countering the OTP phishing attack pattern.

> *Note: Step-up authentication is documented here as an architectural recommendation. Full implementation is scoped as future work requiring integration with MoMo provider APIs (MTN, Telecel Cash, AirtelTigo Money).*

---

## Key EDA Findings

Exploratory data analysis on the synthetic dataset revealed the following patterns, all of which inform the feature engineering and modelling approach:

**Fraud Amount Patterns:**
Fraudulent transactions are consistently 2.5x to 2.7x higher than legitimate transactions across all income tiers. This validates behavioural baselining as the core detection mechanism — the signal is consistent regardless of whether the victim is low or high income.

**Channel Risk:**
Agent channel carries the highest MoMo fraud rate at 16.8%, consistent with BoG findings on agent vulnerability and insider collusion risks. USSD sits at 4.0% and app at 2.2%.

**Temporal Patterns:**
Fraudulent transactions peak between 1am and 4am. Friday attacks peak at 1am — exploiting freshly loaded payday accounts. Saturday MoMo fraud peaks at 2am, followed by bank fraud peaking at 4am — the two-hour gap is the cross-channel lateral movement pattern in action.

**Regional Distribution:**
Northern region leads MoMo fraud (9.5%). Western region leads bank fraud (18.8%), reflecting the large-scale and artisanal mining economy where miners use MoMo to transfer earnings to urban bank accounts — a legitimate pattern that must not be misclassified.

**Scope Clarification:**
MoneyGuard is specifically focused on the MoMo-bank cross-channel attack surface. Card fraud, internet banking fraud, and ATM skimming are real threat vectors in Ghana's financial ecosystem but fall outside this system's scope. The 0.0% fraud rate on non-MoMo bank channels in the synthetic dataset reflects this deliberate design boundary — not an absence of those attack types in Ghana's real fraud landscape.

**Fairness Warning:**
`location_region` is used only as a contextual feature in MoneyGuard — never as a primary fraud predictor. Using region in isolation would disproportionately flag legitimate transactions from already underserved communities, constituting algorithmic discrimination inconsistent with Ghana's Data Protection Act 2012 (Act 843).

**Note on Ghana's regions:**
This simulation uses Ghana's pre-2019 10-region structure. Ghana reorganised to 16 regions in 2019. A production deployment of MoneyGuard would use the current 16-region structure. Results here remain directionally valid.

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

| Pattern | Description | Real-World Signals |
|---------|-------------|-------------------|
| **OTP Phishing** | Attacker poses as merchant, tricks victim into sharing MoMo authorization code | New device, unusual hour, unknown merchant, OTP requested |
| **Account Takeover (ATO)** | Attacker uses shared PIN to access linked bank account | New device, after-hours, channel switch, rapid transactions |
| **Structured Draining** | Repeated below-personal-threshold withdrawals to evade velocity checks | High velocity, same receiver, amounts just below personal threshold |
| **Cross-Channel Lateral Movement** | MoMo compromise used as entry point to bank account 24–72 hours later | MoMo event linked to bank drain, same accounts, overnight window |

---

## Regulatory Mapping

| Regulation | Jurisdiction | Relevance to MoneyGuard |
|------------|-------------|--------------------------|
| **Anti-Money Laundering Act, 2008 (Act 749)** | Ghana | STR filing obligations; defines suspicious transaction criteria |
| **AML (Amendment) Act, 2014 (Act 874)** | Ghana | Extends obligations to mobile money operators |
| **Payment Systems and Services Act, 2019 (Act 987)** | Ghana | Governs MoMo providers; mandates AML/CFT controls |
| **BoG Consumer Protection Directive, 2022** | Ghana | Customer notification obligations; step-up authentication alignment |
| **Data Protection Act, 2012 (Act 843)** | Ghana | Prohibits discriminatory profiling; governs ML model data use |
| **FATF Recommendation 16** | International | Wire transfer rules; applies to MoMo cross-border transactions |
| **FATF Financial Inclusion Guidance** | International | Supports proportionate, risk-based controls for all income levels |
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
│   ├── 01_eda.ipynb                    # ✅ Complete
│   ├── 02_feature_engineering.ipynb    # In progress
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

| Metric | Baseline (Rules-Only) | MoneyGuard (ML Hybrid) |
|--------|----------------------|------------------------|
| False Negative Rate | TBD | TBD |
| False Positive Rate | TBD | TBD |
| Mean Time to Flag | Days | TBD |
| Cross-Channel Detection | ❌ | ✅ |
| Explainable Alerts | ❌ | ✅ |
| Low-Income User Protection | ❌ | ✅ |
| Weekend Attack Detection | ❌ | ✅ |
| MoMo Fraud Rate (Synthetic) | — | 8.1% |
| Bank Fraud Rate (Synthetic) | — | 12.9% |

---

## Future Work

- **Real-time streaming** via Apache Kafka or AWS Kinesis
- **REST API** via FastAPI for integration with core banking systems
- **Automated customer notification** pipeline (BoG CPD 2022 full compliance)
- **Model retraining pipeline** with drift detection
- **Network graph analysis** for mule account detection
- **SMS alert integration** with MTN, Telecel Cash, and AirtelTigo Money APIs
- **16-region update** to reflect Ghana's current administrative structure
- **Local language support** for step-up authentication prompts

---

## Author


Data Scientist | Business Strategist
Specialising in secure, ethical, and inclusive fintech solutions.

[GitHub](https://github.com/miss-nana/MoneyguardGH)

---

## License

MIT License — see `LICENSE` for details.

---

> *This project uses synthetic data generated to model Ghana's mobile money ecosystem. No real customer data is used. MoneyGuard is an independent academic portfolio project with no affiliation to the Bank of Ghana or any financial institution.*