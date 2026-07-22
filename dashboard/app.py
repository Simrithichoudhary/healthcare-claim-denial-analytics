from pathlib import Path
import sys
import sqlite3

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "claim_denial_pipeline.pkl"
DECISION_THRESHOLD = 0.20

DATABASE_PATH = PROJECT_ROOT / "data" / "healthcare_claims.db"

sys.path.append(str(PROJECT_ROOT / "src"))

from recommendation_engine import generate_recommendations


model_pipeline = joblib.load(MODEL_PATH)

@st.cache_data
def load_claims_data():
    conn = sqlite3.connect(DATABASE_PATH)

    claims = pd.read_sql(
        "SELECT * FROM claims",
        conn
    )

    conn.close()

    return claims


claims = load_claims_data()


st.set_page_config(
    page_title="Healthcare Claim Denial Analytics",
    page_icon="🏥",
    layout="wide",
)

st.markdown(
    """
<div style="padding: 2rem 2rem; border-radius: 14px;
background: linear-gradient(90deg, #0f172a 0%, #1e3a5f 100%);
margin-bottom: 1.5rem;">
<h1 style="color: white; margin: 0; font-size: 2.2rem;">
🏥 Healthcare Claim Denial Analytics
</h1>
<p style="
color:#E2E8F0;
font-size:1.15rem;
margin-top:0.7rem;
margin-bottom:0;
font-weight:400;
">
Historical denial insights, financial impact analysis, and pre-submission claim risk prediction.
</p>
</div>
    """,
    unsafe_allow_html=True
)

st.markdown("## Executive Overview")

st.caption(
    "A high-level summary of historical claim volume, denials, "
    "and associated revenue risk."
)

total_claims = len(claims)
denied_claims = int(claims["was_denied"].sum())
denial_rate = denied_claims / total_claims * 100
revenue_leakage = claims["revenue_leakage"].sum()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="📄 Claims Analyzed",
        value=f"{total_claims:,}",
        help="Total historical claims available for analysis."
    )

with kpi2:
    st.metric(
        label="❌ Denied Claims",
        value=f"{denied_claims:,}",
        help="Claims that were denied by the payer."
    )

with kpi3:
    st.metric(
        label="📉 Historical Denial Rate",
        value=f"{denial_rate:.2f}%",
        help="Percentage of historical claims that were denied."
    )

with kpi4:
    st.metric(
        label="💰 Revenue at Risk",
        value=f"${revenue_leakage / 1_000_000:.2f}M",
        help="Total billed amount associated with denied claims."
    )

st.divider()
st.markdown("## Historical Performance")

st.caption(
    "Analyze historical claim outcomes to identify denial patterns, payer performance, and major revenue risk drivers."
)

payer_analysis = (
    claims.groupby("payer_name")
    .agg(
        total_claims=("claim_id", "count"),
        denied_claims=("was_denied", "sum")
    )
    .reset_index()
)

payer_analysis["denial_rate_pct"] = (
    payer_analysis["denied_claims"]
    / payer_analysis["total_claims"]
    * 100
)

denial_reason_analysis = (
    claims[claims["was_denied"] == 1]
    .groupby("denial_reason")
    .agg(
        denied_claims=("claim_id", "count"),
        revenue_leakage=("revenue_leakage", "sum")
    )
    .reset_index()
    .sort_values("revenue_leakage", ascending=False)
)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    payer_chart = px.bar(
        payer_analysis.sort_values(
            "denial_rate_pct",
            ascending=False
        ),
        x="payer_name",
        y="denial_rate_pct",
        title="Denial Rate by Payer",
        labels={
            "payer_name": "Payer",
            "denial_rate_pct": "Denial Rate (%)"
        }
    )

    st.plotly_chart(
        payer_chart,
        use_container_width=True
    )

with chart_col2:
    denial_reason_chart = px.bar(
        denial_reason_analysis,
        x="revenue_leakage",
        y="denial_reason",
        orientation="h",
        title="Revenue Leakage by Denial Reason",
        labels={
            "revenue_leakage": "Revenue Leakage ($)",
            "denial_reason": "Denial Reason"
        }
    )

    denial_reason_chart.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        denial_reason_chart,
        use_container_width=True
    )

st.divider()

st.markdown("## Claim Risk Prediction")

st.caption(
    "Enter claim details to estimate the probability of claim denial "
    "before submission."
)

col1, col2 = st.columns(2)

with col1:
    payer_name = st.selectbox(
        "Payer Name",
        [
            "Ambetter Marketplace",
            "Humana Medicare Advantage",
            "State Medicaid"
        ]
    )

    plan_type = st.selectbox(
        "Plan Type",
        [
            "Commercial",
            "Medicaid",
            "Medicare Advantage"
        ]
    )

    provider_specialty = st.selectbox(
        "Provider Specialty",
        [
            "Primary Care",
            "Cardiology",
            "Radiology",
            "Orthopedics",
            "Emergency Medicine"
        ]
    )

    cpt_code = st.selectbox(
        "CPT Code",
        ["99213", "99214", "71046", "93000", "73560"]
    )

    icd10_code = st.selectbox(
        "ICD-10 Code",
        ["Z00.00", "I10", "R07.9", "K21.9", "G43.909"]
    )

    claim_amount = st.number_input(
        "Claim Amount ($)",
        min_value=0.0,
        value=500.0,
        step=50.0
    )

    days_to_submit = st.number_input(
        "Days to Submit",
        min_value=0,
        value=5,
        step=1
    )

with col2:
    prior_auth_required = st.selectbox(
        "Prior Authorization Required?",
        ["No", "Yes"]
    )

    prior_auth_on_file = st.selectbox(
        "Prior Authorization on File?",
        ["No", "Yes"]
    )

    documentation_complete = st.selectbox(
        "Documentation Complete?",
        ["No", "Yes"]
    )

    eligibility_verified = st.selectbox(
        "Eligibility Verified?",
        ["No", "Yes"]
    )

    provider_credentialed = st.selectbox(
        "Provider Credentialed?",
        ["No", "Yes"]
    )

    coding_valid = st.selectbox(
        "Coding Valid?",
        ["No", "Yes"]
    )

    duplicate_indicator = st.selectbox(
        "Possible Duplicate Claim?",
        ["No", "Yes"]
    )

if st.button("Analyze Claim Risk"):

    claim_input = pd.DataFrame([{
        "payer_name": payer_name,
        "plan_type": plan_type,
        "provider_specialty": provider_specialty,
        "cpt_code": cpt_code,
        "icd10_code": icd10_code,
        "claim_amount": claim_amount,
        "prior_auth_required": 1 if prior_auth_required == "Yes" else 0,
        "prior_auth_on_file": 1 if prior_auth_on_file == "Yes" else 0,
        "documentation_complete": 1 if documentation_complete == "Yes" else 0,
        "eligibility_verified": 1 if eligibility_verified == "Yes" else 0,
        "provider_credentialed": 1 if provider_credentialed == "Yes" else 0,
        "coding_valid": 1 if coding_valid == "Yes" else 0,
        "duplicate_indicator": 1 if duplicate_indicator == "Yes" else 0,
        "days_to_submit": days_to_submit
    }])

    # The saved pipeline performs encoding and scaling automatically.
    denial_probability = model_pipeline.predict_proba(
        claim_input
    )[0, 1]

    denial_prediction = int(
        denial_probability >= DECISION_THRESHOLD
    )

    st.divider()

    st.markdown("## Pre-Submission Claim Risk Assessment")

    with st.container(border=True):

         st.caption(
             "This assessment estimates the probability of claim denial based on "
             "clinical, operational, and payer-related factors."
        )
         st.metric(
            label="Estimated Probability of Denial",
            value=f"{denial_probability * 100:.1f}%"
        )
         st.caption("Denial Risk Level")
         st.progress(float(denial_probability))
    if denial_probability < 0.10:
        st.success(
            "🟢 **LOW RISK**\n\n"
            "This claim appears suitable for standard submission."
        )

    elif denial_probability < 0.30:
        st.warning(
            "🟡 **MODERATE RISK**\n\n"
            "Review the claim carefully before submission."
        )

    else:
        st.error(
            "🔴 **HIGH RISK**\n\n"
            "Review and resolve the identified issues before submitting "
            "the claim to reduce the likelihood of denial."
        )

    if denial_prediction == 1:
        st.info(
        "This claim exceeds the validated review threshold and "
        "should be reviewed before submission."
    )
    else:
        st.info(
        "This claim falls below the review threshold and appears "
        "suitable for the standard submission workflow."
    )

    st.markdown("### Key Risk Factors Identified")

    risk_factors = []

    if (
        claim_input.iloc[0]["prior_auth_required"] == 1
        and claim_input.iloc[0]["prior_auth_on_file"] == 0
    ):
        risk_factors.append(
            "Prior authorization is required but is not on file."
        )

    if claim_input.iloc[0]["documentation_complete"] == 0:
        risk_factors.append(
            "Required claim documentation is incomplete."
        )

    if claim_input.iloc[0]["eligibility_verified"] == 0:
        risk_factors.append(
            "Patient insurance eligibility has not been verified."
        )

    if claim_input.iloc[0]["provider_credentialed"] == 0:
        risk_factors.append(
            "Provider credentialing has not been confirmed."
        )

    if claim_input.iloc[0]["coding_valid"] == 0:
        risk_factors.append(
            "CPT or ICD-10 coding validation failed."
        )

    if claim_input.iloc[0]["duplicate_indicator"] == 1:
        risk_factors.append(
            "The claim may be a duplicate submission."
        )

    if claim_input.iloc[0]["days_to_submit"] > 30:
        risk_factors.append(
            "The claim has a long submission delay."
        )

    if risk_factors:
        for factor in risk_factors:
            st.write(f"• {factor}")
    else:
        st.write("• No major operational risk factors identified.")

    st.markdown("### Recommended Actions")

    recommendations = generate_recommendations(
        claim_input.iloc[0]
    )

    if recommendations:
        for recommendation in recommendations:
            st.write(f"• {recommendation}")
    else:
        st.write(
        "• No significant operational risks were identified. "
        "Proceed with the standard validation and submission workflow."
    )