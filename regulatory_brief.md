# GhanaGuard — Regulatory Brief

## Overview
This document maps GhanaGuard's detection capabilities to the specific regulatory obligations
of mobile money operators and financial institutions operating in Ghana.

---

## 1. Ghana Anti-Money Laundering Act, 2008 (Act 749) & Amendment Act, 2014 (Act 874)

**Key Obligations:**
- Accountable institutions must file Suspicious Transaction Reports (STRs) with the Financial Intelligence Centre (FIC)
- Transactions that are unusual, have no apparent lawful purpose, or involve structuring to avoid reporting thresholds must be reported
- The 2014 amendment extended these obligations explicitly to mobile money operators

**GhanaGuard Mapping:**
- The risk-tiered alert engine generates STR-ready summaries for HIGH-tier alerts
- Structured draining detection directly targets threshold-evasion behavior referenced in Act 874
- All alerts are timestamped and logged to support FIC filing deadlines

---

## 2. Payment Systems and Services Act, 2019 (Act 987)

**Key Obligations:**
- Payment service providers (including MoMo operators) must implement AML/CFT controls
- Providers must maintain transaction records and make them available to the Bank of Ghana
- Operators must have systems capable of identifying and reporting suspicious activity

**GhanaGuard Mapping:**
- The hybrid ML pipeline provides a documented, auditable AML/CFT control
- Transaction logs are preserved in structured format for regulatory access
- The explainability layer ensures every alert has a documented rationale

---

## 3. Bank of Ghana Consumer Protection Directive, 2022

**Key Obligations:**
- Financial service providers must notify customers of suspicious activity on their accounts
- Customers must be informed of account restrictions or freezes in a timely manner
- Providers must have dispute resolution mechanisms for fraud victims

**GhanaGuard Mapping:**
- The alert engine includes a notification trigger flag on every HIGH and MEDIUM alert
- Future work: automated SMS/email notification pipeline integrated with MoMo provider APIs
- Alert logs support dispute resolution by providing a full transaction timeline

---

## 4. Data Protection Act, 2012 (Act 843)

**Key Obligations:**
- Personal data must be collected for a specified, explicit, and legitimate purpose
- Data subjects must be informed of processing activities
- Data must be kept secure and not transferred without appropriate safeguards

**GhanaGuard Mapping:**
- The system is trained and demonstrated on synthetic data only — no real customer PII is used
- In production deployment, data minimisation principles apply: only transaction metadata, not content, is processed
- Model inputs are documented to support data subject rights requests

---

## 5. FATF Recommendation 16 — Wire Transfers

**Key Obligations:**
- Ordering institutions must include accurate originator and beneficiary information in transfers
- Transfers with missing or incomplete information must be flagged and investigated
- Applies to electronic fund transfers including mobile money

**GhanaGuard Mapping:**
- Cross-channel correlation engine tracks originator-beneficiary pairs across MoMo and bank transfers
- Incomplete or mismatched account information is a feature flag in the model
- HIGH-tier alerts for cross-channel lateral movement are consistent with R.16 investigation triggers

---

## 6. GIABA Mutual Evaluation Framework

Ghana is evaluated periodically by GIABA (Inter-Governmental Action Group against Money Laundering
in West Africa) on its AML/CFT effectiveness. GhanaGuard's documented, explainable approach
supports institutional readiness for mutual evaluation by demonstrating:
- Effectiveness of transaction monitoring controls
- Ability to detect typologies relevant to West Africa (mobile money fraud, structuring)
- Documented compliance culture with audit trails

---

*Last updated: February 2026*
*Author: [Your Name]*
