def generate_recommendations(claim):
    recommendations = []

    if (
        claim["prior_auth_required"] == 1
        and claim["prior_auth_on_file"] == 0
    ):
        recommendations.append(
            "Obtain prior authorization before submitting the claim."
        )

    if claim["documentation_complete"] == 0:
        recommendations.append(
            "Complete and attach all required clinical documentation."
        )

    if claim["eligibility_verified"] == 0:
        recommendations.append(
            "Verify the patient's insurance eligibility and coverage."
        )

    if claim["provider_credentialed"] == 0:
        recommendations.append(
            "Confirm that the provider is credentialed with the payer."
        )

    if claim["coding_valid"] == 0:
        recommendations.append(
            "Review CPT and ICD-10 codes for accuracy and compatibility."
        )

    if claim["duplicate_indicator"] == 1:
        recommendations.append(
            "Review the claim for possible duplicate submission."
        )

    if claim["days_to_submit"] > 30:
        recommendations.append(
            "Expedite submission because the claim has been delayed."
        )

    if not recommendations:
        recommendations.append(
            "No major operational issues detected. Proceed with standard review."
        )

    return recommendations