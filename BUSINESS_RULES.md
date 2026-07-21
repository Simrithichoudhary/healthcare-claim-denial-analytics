# Synthetic Data Business Rules

This project uses **synthetic data only**. No patient, provider, hospital, or payer record is real.

## Core denial drivers

A claim receives a higher denial probability when one or more of these conditions occur:

1. A required prior authorization is missing.
2. Clinical documentation is incomplete.
3. Insurance eligibility was not verified.
4. The provider is not actively credentialed.
5. Coding validation failed.
6. The claim appears to be a duplicate.
7. The claim was submitted more than 60 days after service.
8. Payer and specialty risk differ modestly.
9. Very high-value claims receive a small additional risk adjustment.

The outcome still contains controlled randomness. This prevents the dataset from becoming a simple rules engine where every failed check is always denied.

## Why this design is useful

The model must learn realistic patterns without receiving a perfectly deterministic answer. It also makes it possible to compare:
- diagnostic SQL findings,
- predictive model performance,
- threshold decisions,
- and operational recommendations.

## Guardrails

- `denial_probability_true` exists only to audit the generator. It must **never** be used as a model feature.
- Outcome fields such as `claim_status`, `denial_reason`, `amount_paid`, and `revenue_leakage` must not be used to predict denial.
- All published results must be labeled as synthetic or simulated.
