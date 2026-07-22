🏥 Healthcare Claim Denial Analytics
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end Business Analytics solution that combines data engineering, machine learning, and interactive visualization to identify high-risk healthcare claims before submission.

📌 Project Overview

Healthcare providers lose millions of dollars annually due to denied insurance claims caused by incomplete documentation, coding errors, eligibility issues, and authorization failures.

This project demonstrates how predictive analytics can help revenue cycle teams identify potentially denied claims before submission, allowing operational teams to reduce reimbursement delays and improve financial performance.

The solution combines:

- Historical claim analytics
- Interactive business dashboards
- Machine learning-based denial prediction
- Explainable risk factors
- Actionable operational recommendations

🎯 Business Problems

Insurance claim denials create significant financial and operational challenges for healthcare organizations.

Common denial causes include:

Missing prior authorization
Incomplete documentation
Insurance eligibility issues
Provider credentialing problems
Coding errors
Duplicate claims

Traditional review processes rely heavily on manual validation, making it difficult to proactively identify high-risk claims.

💡 Solution

The application provides two complementary capabilities:

Historical Analytics
Executive KPI dashboard
Denial rate by payer
Revenue at risk
Denial reason analysis
Predictive Analytics

Users enter claim information before submission.

The machine learning model estimates:

Probability of denial
Risk category
Key operational risk factors
Recommended actions

This enables healthcare organizations to intervene before claim submission instead of after denial.

🏗 Solution Architecture
Healthcare Claims Dataset
          │
          ▼
Data Cleaning & Feature Engineering
          │
          ▼
SQLite Database
          │
          ▼
Scikit-Learn Pipeline
(ColumnTransformer +
OneHotEncoder +
StandardScaler +
Logistic Regression)
          │
          ▼
Probability Prediction
          │
          ▼
Streamlit Dashboard
          │
          ▼
Operational Recommendations

🚀 Features
Executive Dashboard
Total claims analyzed
Historical denial rate
Revenue at risk
Denied claims
Historical Analytics
Denial Rate by Payer
Revenue Leakage by Denial Reason
Predictive Analytics
Estimated probability of denial
Risk categorization
Key risk factors
Recommended actions

🛠 Technology Stack
| Category | Technologies |
|----------|--------------|
| Language | Python |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Streamlit |
| Machine Learning | Scikit-learn |
| Model | Logistic Regression |
| Preprocessing | ColumnTransformer, OneHotEncoder, StandardScaler |
| Model Persistence | Joblib |

🤖 Machine Learning Pipeline

The prediction model was implemented using a Scikit-learn Pipeline to ensure consistent preprocessing during both training and inference.

The pipeline includes:

One-hot encoding for categorical variables
Feature scaling for numerical variables
Logistic Regression classifier
Threshold optimization for business use

This approach eliminates training-serving inconsistencies and simplifies deployment.

📊 Model Performance
| Metric | Value |
|--------|------:|
| Accuracy | **87.7%** |
| Precision | **53.97%** |
| Recall (0.20 threshold) | **55.8%** |
| Best F1 Score | **0.432** |
| ROC-AUC | **0.7817** |

Because denied claims represent a smaller proportion of the dataset, accuracy alone does not fully reflect model performance. Greater emphasis was placed on ROC-AUC, precision, recall, and threshold optimization to evaluate how effectively the model identifies claims that may require pre-submission review. The decision threshold was adjusted from the default 0.50 to 0.20 to improve recall while maintaining reasonable precision for a business screening workflow.

🖥 Dashboard Preview
<img width="1330" height="198" alt="Screenshot 2026-07-21 at 6 09 57 PM" src="https://github.com/user-attachments/assets/26c93867-359d-4215-8c16-e68dd82d957b" />

Executive Dashboard
<img width="1192" height="199" alt="Screenshot 2026-07-21 at 6 10 21 PM" src="https://github.com/user-attachments/assets/4889aaa9-b0b5-4dc6-bd5a-4e8faaf70ecf" />

Historical Analytics
<img width="1416" height="548" alt="Screenshot 2026-07-21 at 6 11 22 PM" src="https://github.com/user-attachments/assets/ffc44a1e-ac33-4def-9445-89d3d808a6de" />

High-Risk Prediction
<img width="1406" height="723" alt="Screenshot 2026-07-21 at 6 13 06 PM" src="https://github.com/user-attachments/assets/e3749a44-eb0b-4b09-9711-0b14311baa65" />

Low-Risk Prediction
<img width="1421" height="649" alt="Screenshot 2026-07-21 at 6 13 41 PM" src="https://github.com/user-attachments/assets/87c80eae-d490-4a68-aa41-c930b5166bbd" />

📂 Project Structure
healthcare-claim-denial-analytics/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── healthcare_claims.csv
│   ├── healthcare_claims.db
│   └── data_dictionary.csv
│
├── models/
│   └── claim_denial_pipeline.pkl
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Feature_Engineering.ipynb
│   └── 03_Model_Building.ipynb
│
├── src/
│   ├── generate_data.py
│   ├── recommendation_engine.py
│   └── setup_database.py
│
└── README.md

⚙ Installation
git clone https://github.com/Simrithichoudhary/healthcare-claim-denial-analytics.git

cd healthcare-claim-denial-analytics

pip install -r requirements.txt

streamlit run dashboard/app.py

📈 Business Impact
This project demonstrates how predictive analytics can support healthcare revenue cycle management by enabling operational teams to:
- Identify potentially denied claims before submission
- Highlight operational risk factors
- Prioritize claims for manual review
- Reduce reimbursement delays
- Improve claim quality and operational efficiency

⚠ Limitations
The project uses a synthetic healthcare claims dataset for demonstration purposes.
Performance may differ on real-world payer data.
Logistic Regression was selected for interpretability; more advanced models could improve predictive performance.
Periodic retraining would be required to adapt to evolving payer rules and coding practices.

🔮 Future Enhancements
XGBoost and LightGBM model comparison
SHAP-based feature explanations
Real-time API deployment
User authentication
Claim history tracking
Cloud deployment (AWS/Azure)

👤 Author
Simrithi Choudhary
MS Business Analytics | Iowa State University



