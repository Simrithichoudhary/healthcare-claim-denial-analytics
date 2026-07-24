
from pathlib import Path
import numpy as np
import pandas as pd


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_claims(n_claims: int = 10000, seed: int = 42) -> pd.DataFrame:
    """
    Generate a reproducible synthetic healthcare claims dataset.

    Important:
    - No real patient data is used.
    - Denial outcomes follow explicit business rules plus controlled randomness.
    - The dataset is intended for portfolio/educational analysis only.
    """
    rng = np.random.default_rng(seed)

    payers = [
        "BlueShield Commercial",
        "Aetna Commercial",
        "Humana Medicare Advantage",
        "State Medicaid",
        "Ambetter Marketplace",
    ]
    payer_probs = [0.25, 0.20, 0.20, 0.20, 0.15]

    plan_map = {
        "BlueShield Commercial": "Commercial",
        "Aetna Commercial": "Commercial",
        "Humana Medicare Advantage": "Medicare Advantage",
        "State Medicaid": "Medicaid",
        "Ambetter Marketplace": "ACA Marketplace",
    }

    specialties = [
        "Primary Care", "Cardiology", "Orthopedics",
        "Radiology", "Gastroenterology", "Dermatology"
    ]

    cpt_codes = ["99213", "99214", "93000", "71046", "27447", "45378", "70553", "11102"]
    icd10_codes = ["I10", "E11.9", "M17.11", "R07.9", "K21.9", "L30.9", "G43.909", "Z00.00"]

    start_date = np.datetime64("2025-01-01")
    end_date = np.datetime64("2025-12-31")
    date_span = int((end_date - start_date).astype(int))

    df = pd.DataFrame({
        "claim_id": [f"CLM{i:07d}" for i in range(1, n_claims + 1)],
        "patient_id": [f"PAT{x:06d}" for x in rng.integers(1, max(1500, n_claims // 3), n_claims)],
        "provider_id": [f"PRV{x:04d}" for x in rng.integers(1, 151, n_claims)],
        "submission_date": pd.to_datetime(
            start_date + rng.integers(0, date_span + 1, n_claims).astype("timedelta64[D]")
        ),
        "payer_name": rng.choice(payers, size=n_claims, p=payer_probs),
        "provider_specialty": rng.choice(
            specialties, size=n_claims, p=[0.28, 0.15, 0.15, 0.14, 0.14, 0.14]
        ),
        "cpt_code": rng.choice(cpt_codes, size=n_claims),
        "icd10_code": rng.choice(icd10_codes, size=n_claims),
    })

    df["plan_type"] = df["payer_name"].map(plan_map)

    # Claim amounts are positively skewed, as in real billing data.
    specialty_multiplier = df["provider_specialty"].map({
        "Primary Care": 0.55,
        "Cardiology": 1.10,
        "Orthopedics": 1.80,
        "Radiology": 1.25,
        "Gastroenterology": 1.35,
        "Dermatology": 0.75,
    }).astype(float)

    base_amount = rng.lognormal(mean=7.35, sigma=0.75, size=n_claims)
    df["claim_amount"] = np.round(np.clip(base_amount * specialty_multiplier, 90, 30000), 2)

    # Operational fields available before claim submission
    df["prior_auth_required"] = (
        df["cpt_code"].isin(["27447", "70553", "45378"]) |
        df["provider_specialty"].isin(["Orthopedics", "Radiology"])
    ).astype(int)

    auth_success_prob = np.where(df["prior_auth_required"] == 1, 0.84, 0.98)
    df["prior_auth_on_file"] = rng.binomial(1, auth_success_prob)

    df["documentation_complete"] = rng.binomial(
        1,
        np.where(df["provider_specialty"].isin(["Orthopedics", "Cardiology"]), 0.88, 0.93)
    )

    payer_eligibility_prob = df["payer_name"].map({
        "BlueShield Commercial": 0.95,
        "Aetna Commercial": 0.95,
        "Humana Medicare Advantage": 0.92,
        "State Medicaid": 0.88,
        "Ambetter Marketplace": 0.86,
    }).astype(float)
    df["eligibility_verified"] = rng.binomial(1, payer_eligibility_prob)

    df["provider_credentialed"] = rng.binomial(1, 0.97, n_claims)
    df["coding_valid"] = rng.binomial(
        1,
        np.where(df["cpt_code"].isin(["27447", "70553", "45378"]), 0.90, 0.95)
    )
    df["duplicate_indicator"] = rng.binomial(1, 0.015, n_claims)
    df["days_to_submit"] = np.clip(
        np.round(rng.gamma(shape=2.2, scale=6.0, size=n_claims)), 0, 120
    ).astype(int)

    # Denial probability: explicit business rules plus payer/specialty effects.
    logit = np.full(n_claims, -3.05)

    logit += ((df["prior_auth_required"] == 1) & (df["prior_auth_on_file"] == 0)) * 2.15
    logit += (df["documentation_complete"] == 0) * 1.30
    logit += (df["eligibility_verified"] == 0) * 1.05
    logit += (df["provider_credentialed"] == 0) * 1.45
    logit += (df["coding_valid"] == 0) * 1.20
    logit += (df["duplicate_indicator"] == 1) * 2.05
    logit += (df["days_to_submit"] > 60) * 1.80
    logit += (df["claim_amount"] > 10000) * 0.25

    logit += df["payer_name"].map({
        "BlueShield Commercial": -0.15,
        "Aetna Commercial": -0.25,
        "Humana Medicare Advantage": 0.20,
        "State Medicaid": 0.40,
        "Ambetter Marketplace": 0.55,
    }).astype(float)

    logit += df["provider_specialty"].map({
        "Primary Care": -0.15,
        "Cardiology": 0.05,
        "Orthopedics": 0.20,
        "Radiology": 0.20,
        "Gastroenterology": 0.10,
        "Dermatology": -0.05,
    }).astype(float)

    denial_probability = sigmoid(logit)
    df["was_denied"] = rng.binomial(1, denial_probability)
    df["denial_probability_true"] = np.round(denial_probability, 4)

    # Assign the most plausible reason among failed checks.
    denial_reasons = []
    for row in df.itertuples(index=False):
        if row.was_denied == 0:
            denial_reasons.append("Not Denied")
        elif row.duplicate_indicator == 1:
            denial_reasons.append("Duplicate Claim")
        elif row.days_to_submit > 60:
            denial_reasons.append("Timely Filing")
        elif row.prior_auth_required == 1 and row.prior_auth_on_file == 0:
            denial_reasons.append("Prior Authorization Missing")
        elif row.provider_credentialed == 0:
            denial_reasons.append("Provider Credentialing")
        elif row.eligibility_verified == 0:
            denial_reasons.append("Eligibility Issue")
        elif row.coding_valid == 0:
            denial_reasons.append("Coding Error")
        elif row.documentation_complete == 0:
            denial_reasons.append("Documentation Incomplete")
        else:
            denial_reasons.append("Medical Necessity / Other")

    df["denial_reason"] = denial_reasons

    carc_mapping = {
    "Not Denied": None,
    "Prior Authorization Missing": "CO-197",
    "Eligibility Issue": "CO-27",
    "Documentation Incomplete": "CO-16",
    "Coding Error": "CO-4",
    "Duplicate Claim": "CO-18",
    "Timely Filing": "CO-29",
    "Provider Credentialing": "CO-170",
    "Medical Necessity / Other": "CO-50"
    }

    df["carc_code"] = df["denial_reason"].map(carc_mapping)
    soft_denials = {
    "Prior Authorization Missing",
    "Eligibility Issue",
    "Documentation Incomplete",
    "Coding Error",
    "Duplicate Claim",
    "Timely Filing",
    "Provider Credentialing"
    }

    df["denial_type"] = np.where(
        df["denial_reason"] == "Not Denied",
        "Not Applicable",
    np.where(
        df["denial_reason"].isin(soft_denials),
        "Soft",
        "Hard"
    )
    )
    workflow_mapping = {
    "Not Denied": "Claim Approved",
    "Eligibility Issue": "Registration & Eligibility",
    "Prior Authorization Missing": "Authorization",
    "Documentation Incomplete": "Clinical Documentation",
    "Coding Error": "Medical Coding",
    "Duplicate Claim": "Billing",
    "Timely Filing": "Billing",
    "Provider Credentialing": "Provider Enrollment",
    "Medical Necessity / Other": "Clinical Review"
    }

    df["workflow_stage"] = df["denial_reason"].map(workflow_mapping)

    df["claim_status"] = np.where(df["was_denied"] == 1, "Denied", "Approved")
    # Payment behavior: approved claims can still be underpaid.
    allowed_ratio = np.clip(rng.normal(0.83, 0.08, n_claims), 0.55, 1.0)
    underpayment_factor = np.where(rng.random(n_claims) < 0.16, rng.uniform(0.70, 0.93, n_claims), 1.0)
    df["amount_paid"] = np.where(
        df["was_denied"] == 1,
        0,
        np.round(df["claim_amount"] * allowed_ratio * underpayment_factor, 2)
    )
    df["revenue_leakage"] = np.round(df["claim_amount"] - df["amount_paid"], 2)

    # Organize fields for analysis and modeling.
    columns = [
        "claim_id", "patient_id", "provider_id", "submission_date",
        "payer_name", "plan_type", "provider_specialty", "cpt_code", "icd10_code",
        "claim_amount", "prior_auth_required", "prior_auth_on_file",
        "documentation_complete", "eligibility_verified", "provider_credentialed",
        "coding_valid", "duplicate_indicator", "days_to_submit",
        "claim_status", "was_denied", "denial_reason", "carc_code",
        "denial_type","workflow_stage",
        "amount_paid", "revenue_leakage", "denial_probability_true"
    ]    
    return df[columns]


if __name__ == "__main__":
    output_path = Path(__file__).resolve().parents[1] / "data" / "healthcare_claims.csv"
    claims = generate_claims(n_claims=10000, seed=42)
    claims.to_csv(output_path, index=False)

    print(f"Created {len(claims):,} synthetic claims at: {output_path}")
    print(f"Denial rate: {claims['was_denied'].mean():.2%}")
    print(f"Total billed: ${claims['claim_amount'].sum():,.0f}")
    print(f"Revenue leakage: ${claims['revenue_leakage'].sum():,.0f}")
