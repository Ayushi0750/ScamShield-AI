def compare_rule_vs_ml(rule_result, ml_result):

    rule_prediction = (
        "SCAM"
        if rule_result["is_scam"]
        else "SAFE"
    )

    ml_prediction = ml_result["ml_prediction"]

    agreement = (
        rule_prediction == ml_prediction
    )

    return {
        "rule_prediction": rule_prediction,
        "ml_prediction": ml_prediction,
        "agreement": agreement
    }