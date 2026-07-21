# Healthcare Claim Denial Analytics

An end-to-end Business Analytics portfolio project that uses SQL and Python to identify claims at risk of denial before submission.

## Phase 1 completed

- Reproducible synthetic claims generator
- 10,000-claim dataset
- Data dictionary
- Documented business rules and modeling guardrails

## Next phase

1. Load the CSV into SQLite.
2. Create normalized SQL tables/views.
3. Run diagnostic SQL:
   - denial reasons by revenue at risk,
   - denial rate by payer,
   - denial trends,
   - revenue leakage.
4. Build the Python model only after the SQL findings justify it.

## Run the generator

```bash
python src/generate_data.py
```

## Important

This project uses synthetic data only and is intended for educational and portfolio use.
