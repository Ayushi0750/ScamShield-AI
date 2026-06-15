from app.ml.predictor import predict_probability


texts = [
    "Work from home internship, earn 50000 per week, no experience needed",
    "We are hiring software engineers for a reputed MNC with full benefits",
    "Click this link to claim your prize money instantly",
]


for i, text in enumerate(texts):
    print("\n==============================")
    print(f"TEST {i+1}")
    print("==============================")

    result = predict_probability(text)

    print("INPUT:", text)
    print("OUTPUT:", result)



texts = [
    "Work from home internship, earn 50000 per week, no experience needed",
    "We are hiring software engineers for a reputed MNC with full benefits",
    "Click this link to claim your prize money instantly",
]


for i, text in enumerate(texts):

    print("\n==============================")
    print(f"TEST {i+1}")
    print("==============================")

    result = predict_probability(text)

    print("INPUT:", text)
    print("OUTPUT:", result)