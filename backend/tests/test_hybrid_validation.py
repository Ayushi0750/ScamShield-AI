from app.ml.classifier import classify_job_text, calculate_hybrid_score
from app.services.rule_engine import analyze_job_text


# -------------------------
# 🧪 FULL TEST DATASET (SCAM + GENUINE)
# -------------------------
test_samples = [
    # 🔴 SCAM CASES
    "Pay ₹999 registration fee to start earning 5000 per day from home",
    "Guaranteed income job! No skills required, earn money fast",
    "Processing fee required before interview selection",

    # 🟡 SUSPICIOUS CASES
    "Work from home opportunity, earn good income with flexible hours",
    "Submit small verification fee to activate your account",

    # 🟢 GENUINE CASES (TASK 8 ADDITION)
    "We are hiring backend developers with 2+ years experience in Java and Spring Boot",
    "Software engineer role at Infosys with structured interview process and benefits",
    "Internship opportunity at TCS for final year students in computer science",
    "Join our office in Bangalore for full-time data analyst position with fixed salary",
    "Amazon is hiring software development engineers with competitive compensation and relocation support"
]


# -------------------------
# 🧠 TEST RUNNER
# -------------------------
def run_hybrid_tests():

    print("\n🔥 HYBRID MODEL VALIDATION STARTED (SCAM + GENUINE)\n")

    for i, text in enumerate(test_samples):

        print(f"\n================ TEST {i+1} ================")
        print("TEXT:", text)

        # -------------------------
        # RULE ENGINE
        # -------------------------
        rule_result = analyze_job_text(text)

        # -------------------------
        # ML ENGINE
        # -------------------------
        ml_result = classify_job_text(text)

        # -------------------------
        # HYBRID SCORE
        # -------------------------
        hybrid_result = calculate_hybrid_score(
            rule_score=rule_result["confidence"],
            ml_score=ml_result["ml_score"]
        )

        # -------------------------
        # PREDICTIONS
        # -------------------------
        rule_pred = "SCAM" if rule_result["confidence"] >= 0.5 else "GENUINE"
        ml_pred = "SCAM" if ml_result["ml_score"] >= 0.5 else "GENUINE"

        # -------------------------
        # AGREEMENT CHECK
        # -------------------------
        if rule_pred == ml_pred:
            agreement = "AGREEMENT"
        else:
            diff = abs(rule_result["confidence"] - ml_result["ml_score"])
            agreement = "CONFLICT" if diff > 0.3 else "PARTIAL"

        # -------------------------
        # OUTPUT
        # -------------------------
        print("\n📊 RESULTS:")
        print("Rule Score:", rule_result["confidence"])
        print("ML Score:", ml_result["ml_score"])
        print("Hybrid Score:", hybrid_result["hybrid_score"])
        print("Risk Level:", hybrid_result["risk_level"])
        print("Agreement:", agreement)
        print("Rule Prediction:", rule_pred)
        print("ML Prediction:", ml_pred)


# -------------------------
# RUN TEST
# -------------------------
if __name__ == "__main__":
    run_hybrid_tests()