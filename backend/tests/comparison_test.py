from app.ml.comparison import compare_rule_vs_ml

rule_result = {
    "is_scam": True
}

ml_result = {
    "ml_prediction": "SCAM"
}

result = compare_rule_vs_ml(
    rule_result,
    ml_result
)

print(result)