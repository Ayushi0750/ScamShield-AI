from app.ml.predictor import predict_probability

test_cases = [

    # Genuine
    "Software Engineer Intern at TCS. Interview required. Apply through official portal.",

    "Data Analyst role. SQL knowledge required. Multiple interview rounds.",

    # Scam
    "Congratulations! Pay 999 registration fee to activate your offer letter.",

    "Earn 5000 per day from home. No experience required. Limited seats available.",

    "Guaranteed income. No skills required. Start earning immediately."
]

for index, text in enumerate(test_cases, start=1):

    print("\n" + "=" * 60)

    print(f"TEST CASE {index}")
    print("TEXT:", text)

    result = predict_probability(text)

    print("\nRESULT:")
    print(result)