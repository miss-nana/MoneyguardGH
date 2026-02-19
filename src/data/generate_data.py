"""
MoneyGuard — Synthetic Data Generator
======================================
Generates realistic Ghana MoMo and bank transactions
including four attack patterns:
  1. OTP Phishing
  2. Account Takeover (ATO)
  3. Structured Draining
  4. Cross-Channel Lateral Movement

Design Note — Inclusive Fraud Detection:
  The GHS 10,000 BoG reporting threshold is a regulatory floor for AML filing,
  not a fraud detection limit. A fixed threshold fails to protect low-income
  users (farmers, traders, market women) whose accounts sit well below it.
  MoneyGuard uses BEHAVIOURAL BASELINING — each customer has a personal
  anomaly threshold relative to their own transaction history. A GHS 400
  withdrawal by a farmer is treated with the same scrutiny as a GHS 9,500
  withdrawal by a business owner. This aligns with FATF financial inclusion
  guidance and the BoG Consumer Protection Directive 2022.

Output:
  data/synthetic/momo_transactions.csv
  data/synthetic/bank_transactions.csv

Usage:
  python src/data/generate_data.py
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# ── Configuration ────────────────────────────────────────────
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
fake = Faker('en_GB')
Faker.seed(SEED)

NUM_CUSTOMERS  = 500
NUM_MOMO_LEGIT = 8000
NUM_BANK_LEGIT = 4000
NUM_ATTACKS    = 120
OUTPUT_DIR     = "data/synthetic"

# BoG regulatory reporting floor — used for structured drain detection only
# NOT used as the primary fraud detection threshold
BOG_REPORTING_THRESHOLD = 10000

REGIONS = [
    "Greater Accra", "Ashanti", "Western", "Eastern",
    "Central", "Northern", "Volta", "Upper East", "Upper West", "Brong-Ahafo"
]

# Income tiers — reflects Ghana's socioeconomic reality
INCOME_TIERS = {
    "low":    {"min": 300,   "max": 800},    # farmers, traders, casual workers
    "middle": {"min": 800,   "max": 3000},   # salaried workers, small business
    "high":   {"min": 3000,  "max": 15000},  # professionals, large business
}

INCOME_TIER_WEIGHTS = [0.55, 0.35, 0.10]    # 55% low-income — reflects Ghana's reality

MERCHANT_CATEGORIES = ["food", "utility", "retail", "airtime", "transfer", "unknown"]
MOMO_TX_TYPES       = ["send", "receive", "withdraw", "airtime", "bill_payment", "transfer"]
BANK_TX_TYPES       = ["transfer", "withdrawal", "deposit", "momo_link"]
MOMO_CHANNELS       = ["ussd", "app", "agent"]
BANK_CHANNELS       = ["mobile", "internet", "atm", "branch", "momo"]


# ── Helper Functions ──────────────────────────────────────────

def generate_customer_profiles(n):
    """
    Create a pool of customers with behavioural baselines.
    Income tiers reflect Ghana's socioeconomic distribution —
    55% low-income, 35% middle, 10% high.
    Each customer's anomaly threshold is personal, not universal.
    """
    customers = []
    for i in range(n):
        tier      = random.choices(list(INCOME_TIERS.keys()), INCOME_TIER_WEIGHTS)[0]
        tier_data = INCOME_TIERS[tier]
        typical_amount = round(random.uniform(tier_data["min"], tier_data["max"]), 2)

        customers.append({
            "customer_id":           f"CUST-GH-{i:05d}",
            "momo_account":          f"MOMO-GH-{i:05d}",
            "bank_account":          f"BANK-GH-{i:05d}" if random.random() > 0.2 else None,
            "region":                random.choice(REGIONS),
            "income_tier":           tier,
            "typical_amount_ghs":    typical_amount,
            # Personal anomaly threshold — 3x typical transaction
            # This is what MoneyGuard uses, not the BoG GHS 10,000 floor
            "personal_alert_threshold": round(typical_amount * 3, 2),
            "typical_channel":       random.choice(MOMO_CHANNELS),
            "typical_tx_hour":       random.randint(8, 20),
            "monthly_tx_count":      random.randint(5, 60),
            "pin":                   f"{random.randint(1000, 9999)}",
        })
    return customers


def random_timestamp(start_days_ago=90, end_days_ago=0):
    """Generate a random timestamp within a window."""
    start = datetime.now() - timedelta(days=start_days_ago)
    end   = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def amount_above_personal_threshold(customer, multiplier=3.5):
    """
    Generate a fraudulent amount that exceeds the customer's personal threshold.
    For a low-income farmer (typical: GHS 400), this might be GHS 1,400.
    For a high-income professional (typical: GHS 8,000), this might be GHS 28,000.
    Both are equally suspicious relative to their baseline.
    """
    return round(customer["typical_amount_ghs"] * multiplier, 2)


def amount_structured_below_personal_threshold(customer):
    """
    Generate structured draining amounts just below the customer's personal threshold.
    Attacker keeps each hit below the radar — but MoneyGuard detects the pattern.
    """
    threshold = customer["personal_alert_threshold"]
    return round(random.uniform(threshold * 0.7, threshold * 0.9), 2)


# ── Legitimate Transaction Generators ────────────────────────

def generate_legit_momo(customers, n):
    """Generate n legitimate MoMo transactions."""
    records = []
    for _ in range(n):
        customer     = random.choice(customers)
        counterparty = random.choice(customers)
        ts     = random_timestamp()
        amount = round(
            abs(np.random.normal(customer["typical_amount_ghs"],
                                 customer["typical_amount_ghs"] * 0.3)), 2
        )
        records.append({
            "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              ts,
            "sender_account":         customer["momo_account"],
            "receiver_account":       counterparty["momo_account"],
            "amount_ghs":             amount,
            "transaction_type":       random.choice(MOMO_TX_TYPES),
            "channel":                customer["typical_channel"],
            "agent_id":               f"AGT-{customer['region'].replace(' ', '')}-{random.randint(1,99):04d}"
                                      if customer["typical_channel"] == "agent" else None,
            "merchant_category":      random.choice(MERCHANT_CATEGORIES),
            "location_region":        customer["region"],
            "device_id":              f"DEV-{fake.md5()[:6]}",
            "is_new_device":          False,
            "otp_requested":          random.random() > 0.8,
            "linked_bank_account":    customer["bank_account"],
            "income_tier":            customer["income_tier"],
            "personal_alert_threshold": customer["personal_alert_threshold"],
            "label":                  0,
            "attack_type":            "none",
        })
    return records


def generate_legit_bank(customers, n):
    """Generate n legitimate bank transactions."""
    records        = []
    bank_customers = [c for c in customers if c["bank_account"]]
    for _ in range(n):
        customer     = random.choice(bank_customers)
        counterparty = random.choice(bank_customers)
        ts     = random_timestamp()
        amount = round(
            abs(np.random.normal(customer["typical_amount_ghs"] * 2,
                                 customer["typical_amount_ghs"] * 0.5)), 2
        )
        balance_before = round(random.uniform(
            customer["typical_amount_ghs"],
            customer["typical_amount_ghs"] * 10
        ), 2)
        records.append({
            "transaction_id":         f"BANK-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              ts,
            "account_id":             customer["bank_account"],
            "linked_momo_account":    customer["momo_account"],
            "amount_ghs":             amount,
            "transaction_type":       random.choice(BANK_TX_TYPES),
            "channel":                random.choice(BANK_CHANNELS),
            "counterparty_account":   counterparty["bank_account"],
            "balance_before_ghs":     balance_before,
            "balance_after_ghs":      round(balance_before - amount, 2),
            "location_region":        customer["region"],
            "is_after_hours":         False,
            "income_tier":            customer["income_tier"],
            "personal_alert_threshold": customer["personal_alert_threshold"],
            "label":                  0,
            "attack_type":            "none",
        })
    return records


# ── Attack Pattern Generators ─────────────────────────────────

def inject_otp_phishing(customers, n=30):
    """
    Attack Pattern 1: OTP Phishing
    Attacker poses as merchant, tricks victim into sharing OTP.
    Amount exceeds victim's PERSONAL threshold — not the BoG GHS 10,000 floor.
    A GHS 1,200 hit on a farmer is flagged just as a GHS 25,000 hit on an executive.
    Signals: new device, unusual hour, unknown merchant, OTP requested.
    """
    records = []
    for _ in range(n):
        victim           = random.choice(customers)
        attacker_account = f"MOMO-ATK-{random.randint(10000, 99999)}"
        ts               = random_timestamp(start_days_ago=30)
        ts               = ts.replace(hour=random.randint(22, 23))
        amount           = amount_above_personal_threshold(victim)

        records.append({
            "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              ts,
            "sender_account":         victim["momo_account"],
            "receiver_account":       attacker_account,
            "amount_ghs":             amount,
            "transaction_type":       "send",
            "channel":                "ussd",
            "agent_id":               None,
            "merchant_category":      "unknown",
            "location_region":        victim["region"],
            "device_id":              f"DEV-{fake.md5()[:6]}",
            "is_new_device":          True,
            "otp_requested":          True,
            "linked_bank_account":    victim["bank_account"],
            "income_tier":            victim["income_tier"],
            "personal_alert_threshold": victim["personal_alert_threshold"],
            "label":                  1,
            "attack_type":            "otp_phishing",
        })
    return records


def inject_account_takeover(customers, n=30):
    """
    Attack Pattern 2: Account Takeover (ATO)
    Attacker uses shared PIN to access linked bank account.
    Amounts scaled to victim's income tier.
    Signals: new device, after-hours, channel switch, rapid successive transactions.
    """
    momo_records   = []
    bank_records   = []
    bank_customers = [c for c in customers if c["bank_account"]]

    for _ in range(n):
        victim         = random.choice(bank_customers)
        ts             = random_timestamp(start_days_ago=30)
        ts             = ts.replace(hour=random.randint(1, 5))
        amount         = amount_above_personal_threshold(victim)
        balance_before = round(victim["typical_amount_ghs"] * random.uniform(4, 10), 2)

        momo_records.append({
            "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              ts,
            "sender_account":         victim["momo_account"],
            "receiver_account":       f"MOMO-ATK-{random.randint(10000, 99999)}",
            "amount_ghs":             amount,
            "transaction_type":       "transfer",
            "channel":                "app",
            "agent_id":               None,
            "merchant_category":      "transfer",
            "location_region":        random.choice(REGIONS),
            "device_id":              f"DEV-{fake.md5()[:6]}",
            "is_new_device":          True,
            "otp_requested":          False,
            "linked_bank_account":    victim["bank_account"],
            "income_tier":            victim["income_tier"],
            "personal_alert_threshold": victim["personal_alert_threshold"],
            "label":                  1,
            "attack_type":            "account_takeover",
        })

        bank_ts = ts + timedelta(hours=random.randint(24, 72))
        bank_records.append({
            "transaction_id":         f"BANK-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              bank_ts,
            "account_id":             victim["bank_account"],
            "linked_momo_account":    victim["momo_account"],
            "amount_ghs":             amount,
            "transaction_type":       "transfer",
            "channel":                "momo",
            "counterparty_account":   victim["momo_account"],
            "balance_before_ghs":     balance_before,
            "balance_after_ghs":      round(balance_before - amount, 2),
            "location_region":        random.choice(REGIONS),
            "is_after_hours":         True,
            "income_tier":            victim["income_tier"],
            "personal_alert_threshold": victim["personal_alert_threshold"],
            "label":                  1,
            "attack_type":            "account_takeover",
        })

    return momo_records, bank_records


def inject_structured_draining(customers, n=30):
    """
    Attack Pattern 3: Structured Draining
    Multiple below-personal-threshold withdrawals to evade detection.
    For a low-income farmer, this might be 5 x GHS 280 hits.
    For a high-income professional, this might be 5 x GHS 7,000 hits.
    Both patterns are detected by MoneyGuard through velocity + behavioural analysis.
    Signals: repeated amounts just below personal threshold, same receiver, high velocity.
    """
    momo_records   = []
    bank_records   = []
    bank_customers = [c for c in customers if c["bank_account"]]

    for _ in range(n):
        victim         = random.choice(bank_customers)
        attacker_momo  = f"MOMO-ATK-{random.randint(10000, 99999)}"
        base_ts        = random_timestamp(start_days_ago=30)
        balance_before = round(victim["typical_amount_ghs"] * random.uniform(5, 12), 2)
        num_hits       = random.randint(3, 8)

        for hit in range(num_hits):
            hit_ts = base_ts + timedelta(minutes=random.randint(5, 30) * hit)
            amount = amount_structured_below_personal_threshold(victim)

            bank_records.append({
                "transaction_id":         f"BANK-TXN-{fake.unique.random_int(min=100000, max=999999)}",
                "timestamp":              hit_ts,
                "account_id":             victim["bank_account"],
                "linked_momo_account":    victim["momo_account"],
                "amount_ghs":             amount,
                "transaction_type":       "transfer",
                "channel":                "momo",
                "counterparty_account":   victim["momo_account"],
                "balance_before_ghs":     round(balance_before - (amount * hit), 2),
                "balance_after_ghs":      round(balance_before - (amount * (hit + 1)), 2),
                "location_region":        victim["region"],
                "is_after_hours":         hit_ts.hour > 22 or hit_ts.hour < 6,
                "income_tier":            victim["income_tier"],
                "personal_alert_threshold": victim["personal_alert_threshold"],
                "label":                  1,
                "attack_type":            "structured_drain",
            })

            momo_records.append({
                "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
                "timestamp":              hit_ts + timedelta(minutes=random.randint(1, 10)),
                "sender_account":         victim["momo_account"],
                "receiver_account":       attacker_momo,
                "amount_ghs":             amount,
                "transaction_type":       "withdraw",
                "channel":                "agent",
                "agent_id":               f"AGT-{random.choice(REGIONS).replace(' ','')}-{random.randint(1,99):04d}",
                "merchant_category":      "unknown",
                "location_region":        random.choice(REGIONS),
                "device_id":              f"DEV-{fake.md5()[:6]}",
                "is_new_device":          True,
                "otp_requested":          False,
                "linked_bank_account":    victim["bank_account"],
                "income_tier":            victim["income_tier"],
                "personal_alert_threshold": victim["personal_alert_threshold"],
                "label":                  1,
                "attack_type":            "structured_drain",
            })

    return momo_records, bank_records


def inject_lateral_movement(customers, n=30):
    """
    Attack Pattern 4: Cross-Channel Lateral Movement
    MoMo compromise used as entry point to drain linked bank account days later.
    This directly models the real-world case that motivated this project.
    Amounts scaled to victim's income tier — protects low-income users equally.
    Signals: MoMo event followed by bank drain 24-72 hours later, same linked accounts.
    """
    momo_records   = []
    bank_records   = []
    bank_customers = [c for c in customers if c["bank_account"]]

    for _ in range(n):
        victim         = random.choice(bank_customers)
        attacker_momo  = f"MOMO-ATK-{random.randint(10000, 99999)}"
        stage1_ts      = random_timestamp(start_days_ago=30)
        stage1_ts      = stage1_ts.replace(hour=random.randint(18, 22))
        # Stage 1 is a small hit — below suspicion on its own
        amount_stage1  = round(victim["typical_amount_ghs"] * 0.8, 2)
        balance_before = round(victim["typical_amount_ghs"] * random.uniform(4, 10), 2)

        # Stage 1 — MoMo compromise
        momo_records.append({
            "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
            "timestamp":              stage1_ts,
            "sender_account":         victim["momo_account"],
            "receiver_account":       attacker_momo,
            "amount_ghs":             amount_stage1,
            "transaction_type":       "send",
            "channel":                "ussd",
            "agent_id":               None,
            "merchant_category":      "unknown",
            "location_region":        victim["region"],
            "device_id":              f"DEV-{fake.md5()[:6]}",
            "is_new_device":          True,
            "otp_requested":          True,
            "linked_bank_account":    victim["bank_account"],
            "income_tier":            victim["income_tier"],
            "personal_alert_threshold": victim["personal_alert_threshold"],
            "label":                  1,
            "attack_type":            "lateral_movement",
        })

        # Stage 2 — Bank drain 24–72 hours later
        num_bank_hits = random.randint(2, 5)
        for hit in range(num_bank_hits):
            stage2_ts     = stage1_ts + timedelta(hours=random.randint(24, 72))
            stage2_ts     = stage2_ts.replace(hour=random.randint(1, 4))
            amount_stage2 = amount_above_personal_threshold(victim, multiplier=2.5)

            bank_records.append({
                "transaction_id":         f"BANK-TXN-{fake.unique.random_int(min=100000, max=999999)}",
                "timestamp":              stage2_ts,
                "account_id":             victim["bank_account"],
                "linked_momo_account":    victim["momo_account"],
                "amount_ghs":             amount_stage2,
                "transaction_type":       "transfer",
                "channel":                "momo",
                "counterparty_account":   victim["momo_account"],
                "balance_before_ghs":     round(balance_before - (amount_stage2 * hit), 2),
                "balance_after_ghs":      round(balance_before - (amount_stage2 * (hit + 1)), 2),
                "location_region":        random.choice(REGIONS),
                "is_after_hours":         True,
                "income_tier":            victim["income_tier"],
                "personal_alert_threshold": victim["personal_alert_threshold"],
                "label":                  1,
                "attack_type":            "lateral_movement",
            })

            momo_records.append({
                "transaction_id":         f"MOMO-TXN-{fake.unique.random_int(min=100000, max=999999)}",
                "timestamp":              stage2_ts + timedelta(minutes=random.randint(2, 15)),
                "sender_account":         victim["momo_account"],
                "receiver_account":       attacker_momo,
                "amount_ghs":             amount_stage2,
                "transaction_type":       "withdraw",
                "channel":               "agent",
                "agent_id":               f"AGT-{random.choice(REGIONS).replace(' ','')}-{random.randint(1,99):04d}",
                "merchant_category":      "unknown",
                "location_region":        random.choice(REGIONS),
                "device_id":              f"DEV-{fake.md5()[:6]}",
                "is_new_device":          True,
                "otp_requested":          False,
                "linked_bank_account":    victim["bank_account"],
                "income_tier":            victim["income_tier"],
                "personal_alert_threshold": victim["personal_alert_threshold"],
                "label":                  1,
                "attack_type":            "lateral_movement",
            })

    return momo_records, bank_records


# ── Main Pipeline ─────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  MoneyGuard — Synthetic Data Generator")
    print("=" * 55)

    print(f"\n[1/6] Generating {NUM_CUSTOMERS} customer profiles...")
    customers = generate_customer_profiles(NUM_CUSTOMERS)

    # Show income tier distribution
    tiers = [c["income_tier"] for c in customers]
    print(f"       Income tiers — Low: {tiers.count('low')} | "
          f"Middle: {tiers.count('middle')} | High: {tiers.count('high')}")

    print(f"[2/6] Generating {NUM_MOMO_LEGIT} legitimate MoMo transactions...")
    momo_legit = generate_legit_momo(customers, NUM_MOMO_LEGIT)

    print(f"[3/6] Generating {NUM_BANK_LEGIT} legitimate bank transactions...")
    bank_legit = generate_legit_bank(customers, NUM_BANK_LEGIT)

    print(f"[4/6] Injecting attack patterns ({NUM_ATTACKS} sequences)...")
    n = NUM_ATTACKS // 4

    momo_otp                   = inject_otp_phishing(customers, n)
    momo_ato, bank_ato         = inject_account_takeover(customers, n)
    momo_drain, bank_drain     = inject_structured_draining(customers, n)
    momo_lateral, bank_lateral = inject_lateral_movement(customers, n)

    print("[5/6] Combining and saving datasets...")
    all_momo = momo_legit + momo_otp + momo_ato + momo_drain + momo_lateral
    all_bank = bank_legit + bank_ato + bank_drain + bank_lateral

    momo_df = pd.DataFrame(all_momo).sort_values("timestamp").reset_index(drop=True)
    bank_df = pd.DataFrame(all_bank).sort_values("timestamp").reset_index(drop=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    momo_df.to_csv(os.path.join(OUTPUT_DIR, "momo_transactions.csv"), index=False)
    bank_df.to_csv(os.path.join(OUTPUT_DIR, "bank_transactions.csv"), index=False)

    print("[6/6] Done!\n")
    print("=" * 55)
    print(f"  MoMo transactions : {len(momo_df):,}")
    print(f"    └─ Legitimate   : {(momo_df['label'] == 0).sum():,}")
    print(f"    └─ Fraudulent   : {(momo_df['label'] == 1).sum():,}")
    print(f"\n  Bank transactions : {len(bank_df):,}")
    print(f"    └─ Legitimate   : {(bank_df['label'] == 0).sum():,}")
    print(f"    └─ Fraudulent   : {(bank_df['label'] == 1).sum():,}")
    print(f"\n  Saved to  : {OUTPUT_DIR}/")
    print(f"  BoG floor : GHS {BOG_REPORTING_THRESHOLD:,} (regulatory floor only)")
    print(f"  Detection : Behavioural baselining per customer income tier")
    print("=" * 55)


if __name__ == "__main__":
    main()
