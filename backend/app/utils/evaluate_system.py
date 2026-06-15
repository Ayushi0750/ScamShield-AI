import json


def evaluate_system():
    logs = []

    
    with open("./evaluation_logs.json", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            logs.append(json.loads(line))

    total = len(logs)

    TP = FP = TN = FN = 0
    valid_samples = 0

    
    for log in logs:

        prediction = log.get("prediction")
        actual = log.get("actual_label")

        
        if not actual:
            continue

        prediction = prediction.upper().strip()
        actual = actual.upper().strip()

        valid_samples += 1

        if prediction == "SCAM" and actual == "SCAM":
            TP += 1

        elif prediction == "SCAM" and actual == "GENUINE":
            FP += 1

        elif prediction == "GENUINE" and actual == "GENUINE":
            TN += 1

        elif prediction == "GENUINE" and actual == "SCAM":
            FN += 1

    accuracy = (TP + TN) / valid_samples if valid_samples else 0
    precision = TP / (TP + FP) if (TP + FP) else 0
    recall = TP / (TP + FN) if (TP + FN) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    # -----------------------------
    # REPORT
    # -----------------------------
    print("\n FINAL EVALUATION REPORT")
    print("--------------------------------")
    print("Total Logs:", total)
    print("Valid Labeled Samples:", valid_samples)
    print("--------------------------------")
    print("TP:", TP, "FP:", FP, "TN:", TN, "FN:", FN)
    print("--------------------------------")
    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))


if __name__ == "__main__":
    evaluate_system()