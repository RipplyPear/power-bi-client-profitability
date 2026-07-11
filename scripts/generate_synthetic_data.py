"""Generate a reproducible, fictional retail-banking dataset.

The script uses only Python's standard library. All persons and observations
are synthetic; no source values from the internship dataset are copied.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass, replace
from datetime import date, timedelta
from pathlib import Path


DEFAULT_SEED = 20260711
DEFAULT_CLIENTS = 4_000
MONTH_ENDS = (
    date(2024, 1, 31), date(2024, 2, 29), date(2024, 3, 31),
    date(2024, 4, 30), date(2024, 5, 31), date(2024, 6, 30),
    date(2024, 7, 31), date(2024, 8, 31), date(2024, 9, 30),
    date(2024, 10, 31), date(2024, 11, 30), date(2024, 12, 31),
)

COUNTIES = (
    "Bucuresti", "Cluj", "Timis", "Iasi", "Constanta", "Brasov",
    "Prahova", "Dolj", "Sibiu", "Galati",
)
AGE_BUCKETS = ("18-24", "25-34", "35-49", "50-64", "65+")
AGE_WEIGHTS = (0.10, 0.23, 0.34, 0.24, 0.09)
EDUCATION = ("High School", "Post-secondary", "Bachelor", "Master", "Doctorate")
MARITAL = ("Single", "Married", "Divorced")


@dataclass(frozen=True)
class Profile:
    client_id: str
    gender: str
    age_bucket: str
    marital_status: str
    education_level: str
    county: str
    onboarding_channel: str
    onboarding_method: str
    customer_segment: str
    registration_date: date


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def weighted_choice(rng: random.Random, values: tuple[str, ...], weights: tuple[float, ...]) -> str:
    return rng.choices(values, weights=weights, k=1)[0]


def random_registration_date(rng: random.Random) -> date:
    start = date(2018, 1, 1)
    end = date(2023, 12, 31)
    return start + timedelta(days=rng.randint(0, (end - start).days))


def make_profile(rng: random.Random, index: int) -> Profile:
    age = weighted_choice(rng, AGE_BUCKETS, AGE_WEIGHTS)
    digital_probability = {
        "18-24": 0.89, "25-34": 0.86, "35-49": 0.73,
        "50-64": 0.55, "65+": 0.31,
    }[age]
    onboarding_channel = "Digital" if rng.random() < digital_probability else "Branch"
    premium_probability = {
        "18-24": 0.08, "25-34": 0.18, "35-49": 0.30,
        "50-64": 0.29, "65+": 0.22,
    }[age]
    marital_weights = {
        "18-24": (0.91, 0.08, 0.01), "25-34": (0.55, 0.41, 0.04),
        "35-49": (0.27, 0.62, 0.11), "50-64": (0.17, 0.64, 0.19),
        "65+": (0.20, 0.58, 0.22),
    }[age]
    education_weights = {
        "18-24": (0.43, 0.16, 0.32, 0.08, 0.01),
        "25-34": (0.24, 0.12, 0.40, 0.22, 0.02),
        "35-49": (0.29, 0.15, 0.34, 0.19, 0.03),
        "50-64": (0.39, 0.18, 0.28, 0.12, 0.03),
        "65+": (0.48, 0.19, 0.23, 0.07, 0.03),
    }[age]
    return Profile(
        client_id=f"CL{index:05d}",
        gender=rng.choices(("F", "M"), weights=(0.51, 0.49), k=1)[0],
        age_bucket=age,
        marital_status=weighted_choice(rng, MARITAL, marital_weights),
        education_level=weighted_choice(rng, EDUCATION, education_weights),
        county=rng.choices(COUNTIES, weights=(28, 10, 9, 9, 8, 8, 8, 7, 7, 6), k=1)[0],
        onboarding_channel=onboarding_channel,
        onboarding_method="Self-service" if onboarding_channel == "Digital" else "Assisted",
        customer_segment="Premium" if rng.random() < premium_probability else "Standard",
        registration_date=random_registration_date(rng),
    )


def changed_profile(rng: random.Random, profile: Profile) -> Profile:
    """Create a plausible mid-year SCD2 change without altering demographics."""
    if profile.customer_segment == "Standard" and rng.random() < 0.62:
        return replace(profile, customer_segment="Premium")
    if profile.onboarding_channel == "Branch":
        return replace(profile, onboarding_channel="Digital", onboarding_method="Self-service")
    return replace(profile, customer_segment="Standard")


def poisson(rng: random.Random, mean: float) -> int:
    """Knuth sampler, suitable for the small means used here."""
    limit = math.exp(-mean)
    product = 1.0
    count = 0
    while product > limit:
        count += 1
        product *= rng.random()
    return count - 1


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate(output_dir: Path, clients: int, seed: int) -> None:
    rng = random.Random(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    date_rows = [
        {
            "reference_date": month.isoformat(),
            "month_number": month.month,
            "month_name": month.strftime("%B"),
            "quarter": f"Q{((month.month - 1) // 3) + 1}",
            "year": month.year,
            "year_month": month.strftime("%Y-%m"),
        }
        for month in MONTH_ENDS
    ]

    dimension_rows: list[dict[str, object]] = []
    fact_rows: list[dict[str, object]] = []

    for index in range(1, clients + 1):
        base = make_profile(rng, index)
        has_change = rng.random() < 0.16
        second = changed_profile(rng, base) if has_change else None
        first_key = f"CV{index:05d}-01"
        second_key = f"CV{index:05d}-02"

        versions = [(first_key, base, date(2024, 1, 1), date(2024, 6, 30) if has_change else date(9999, 12, 31))]
        if second is not None:
            versions.append((second_key, second, date(2024, 7, 1), date(9999, 12, 31)))

        for version_key, profile, valid_from, valid_to in versions:
            dimension_rows.append({
                "client_version_id": version_key,
                "client_id": profile.client_id,
                "gender": profile.gender,
                "age_bucket": profile.age_bucket,
                "marital_status": profile.marital_status,
                "education_level": profile.education_level,
                "county": profile.county,
                "onboarding_channel": profile.onboarding_channel,
                "onboarding_method": profile.onboarding_method,
                "customer_segment": profile.customer_segment,
                "registration_date": profile.registration_date.isoformat(),
                "valid_from_date": valid_from.isoformat(),
                "valid_to_date": valid_to.isoformat(),
            })

        customer_affluence = clamp(rng.gauss(1.0, 0.25), 0.45, 1.85)
        digital_affinity = clamp(
            rng.gauss(0.58 if base.onboarding_channel == "Digital" else 0.22, 0.16),
            0.05, 0.98,
        )

        for month_index, month in enumerate(MONTH_ENDS):
            profile = second if has_change and month.month >= 7 else base
            version_key = second_key if has_change and month.month >= 7 else first_key
            premium = profile.customer_segment == "Premium"
            seasonality = (1.05 if month.month in (3, 8, 11, 12) else 0.94 if month.month in (5, 6, 9) else 1.0)
            monthly_noise = clamp(rng.gauss(1.0, 0.10), 0.70, 1.30)
            transaction_mean = (4.3 + 3.5 * digital_affinity + (2.1 if premium else 0.0)) * seasonality
            transaction_count = max(0, poisson(rng, transaction_mean))
            digital_share = clamp(digital_affinity + rng.gauss(0, 0.07), 0.0, 1.0)
            digital_transaction_count = min(transaction_count, round(transaction_count * digital_share))
            average_ticket = (210 + 190 * customer_affluence + (130 if premium else 0)) * monthly_noise
            transaction_volume = round(transaction_count * average_ticket * clamp(rng.gauss(1, 0.16), 0.55, 1.50), 2)
            digital_transaction_volume = round(transaction_volume * digital_share * clamp(rng.gauss(1, 0.08), 0.75, 1.20), 2)
            digital_transaction_volume = min(transaction_volume, digital_transaction_volume)
            app_logins = max(0, poisson(rng, 1.8 + digital_affinity * 8.2))
            digitally_active = digital_transaction_count >= 2

            credit_card = rng.random() < clamp(0.20 + 0.16 * customer_affluence + (0.12 if premium else 0), 0, 0.72)
            secured_loan = rng.random() < (0.13 if profile.age_bucket in ("25-34", "35-49", "50-64") else 0.05)
            unsecured_loan = rng.random() < 0.16
            deposit = rng.random() < clamp(0.13 + 0.20 * customer_affluence + (0.15 if premium else 0), 0, 0.70)
            insurance = rng.random() < (0.18 + (0.12 if secured_loan else 0))
            digital_loan = (secured_loan or unsecured_loan) and digitally_active and rng.random() < 0.35
            product_count = sum((credit_card, secured_loan, unsecured_loan, deposit, insurance))
            income = round(clamp(rng.gauss(3600 * customer_affluence + (2100 if premium else 0), 850), 1200, 15000), 2)
            profitability = round(
                -4.0 + 0.0021 * transaction_volume + 2.7 * product_count
                + (2.2 if digitally_active else -0.8) + (3.8 if premium else 0)
                + rng.gauss(0, 3.1),
                2,
            )

            fact_rows.append({
                "client_id": profile.client_id,
                "client_version_id": version_key,
                "reference_date": month.isoformat(),
                "transaction_count": transaction_count,
                "transaction_volume": f"{transaction_volume:.2f}",
                "digital_transaction_count": digital_transaction_count,
                "digital_transaction_volume": f"{digital_transaction_volume:.2f}",
                "mobile_app_login_count": app_logins,
                "credit_card_count": int(credit_card),
                "secured_loan_count": int(secured_loan),
                "unsecured_loan_count": int(unsecured_loan),
                "product_count": product_count,
                "new_customer_flag": "Y" if profile.registration_date.year == 2024 and profile.registration_date.month == month.month else "N",
                "digitally_active_flag": "Y" if digitally_active else "N",
                "credit_card_flag": "Y" if credit_card else "N",
                "loan_flag": "Y" if secured_loan or unsecured_loan else "N",
                "digital_loan_flag": "Y" if digital_loan else "N",
                "monthly_income": f"{income:.2f}",
                "monthly_profitability": f"{profitability:.2f}",
                "deposit_flag": "Y" if deposit else "N",
                "insurance_flag": "Y" if insurance else "N",
            })

    write_csv(output_dir / "Dim_Date.csv", list(date_rows[0]), date_rows)
    write_csv(output_dir / "Dim_Client.csv", list(dimension_rows[0]), dimension_rows)
    write_csv(output_dir / "Fact_ClientMonthly.csv", list(fact_rows[0]), fact_rows)
    print(f"Generated {clients:,} clients and {len(fact_rows):,} monthly observations in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clients", type=int, default=DEFAULT_CLIENTS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    args = parser.parse_args()
    if args.clients < 1:
        parser.error("--clients must be at least 1")
    generate(args.output, args.clients, args.seed)


if __name__ == "__main__":
    main()
