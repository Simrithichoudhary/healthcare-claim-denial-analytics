#  Healthcare Claim Denial Analytics Dashboard

An end-to-end Business Analytics project that predicts healthcare insurance claim denials using Machine Learning while providing interactive business intelligence dashboards for historical analysis.

---

## Business Problem

Healthcare providers lose millions of dollars every year due to insurance claim denials caused by missing documentation, coding errors, eligibility issues, and prior authorization failures.

This project helps identify high-risk claims before submission, enabling providers to reduce preventable denials and improve revenue cycle efficiency.

---

## Project Objectives

- Predict claim denial probability before submission
- Analyze historical denial trends
- Identify revenue at risk
- Provide interactive business intelligence dashboards
- Support proactive operational decision-making

---

## Technology Stack

| Category | Tools |
|----------|-------|
| Programming | Python |
| Database | SQLite |
| Querying | SQL |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (Logistic Regression) |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Model Storage | Joblib |

---

##  Project Structure

```text
healthcare-claim-denial-analytics/
│
├── dashboard/
├── data/
├── models/
├── notebooks/
├── sql/
├── src/
├── BUSINESS_RULES.md
├── requirements.txt
└── README.md
```

---

##  Dashboard Features

- Executive KPI Dashboard
- Historical Claim Analytics
- Denial Rate by Insurance Payer
- Revenue at Risk Analysis
- Pre-Submission Risk Assessment
- Recommended Actions

---

## Machine Learning Pipeline

```text
Historical Claims
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Train/Test Split
        │
        ▼
Logistic Regression Model
        │
        ▼
Probability Prediction
        │
        ▼
Interactive Streamlit Dashboard
```

---

## Business Impact

This solution enables healthcare organizations to:

- Reduce preventable claim denials
- Improve reimbursement cycle efficiency
- Prioritize high-risk claims
- Monitor payer performance
- Support data-driven decision-making

---

## Future Enhancements

- Explainable AI (SHAP)
- XGBoost model comparison
- Real-time EHR integration
- Azure cloud deployment
- Role-based authentication

---

## Installation

```bash
git clone https://github.com/Simrithichoudhary/healthcare-claim-denial-analytics.git

cd healthcare-claim-denial-analytics

pip install -r requirements.txt

streamlit run dashboard/app.py
```

---

## Author

**Simrithi Choudhary**

MS in Business Analytics  
Business Analyst | Data Analyst | SQL | Python | Machine Learning
