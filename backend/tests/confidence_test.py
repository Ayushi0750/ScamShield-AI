from app.ml.predictor import predict_probability

test_cases = [
    "Software Engineer at Google.",
    "Pay registration fee to get selected.",
    "Earn 10000 per day from home.",
    "Python Developer role with interview rounds.",
    "Guaranteed income with no skills required."
]

for text in test_cases:

    result = predict_probability(text)

    print("\n" + "=" * 60)
    print("TEXT:", text)

    print(
        f"Genuine: {result['genuine_probability']}"
    )

    print(
        f"Scam: {result['scam_probability']}"
    )

    print(
        f"Prediction: {result['prediction']}"
    )