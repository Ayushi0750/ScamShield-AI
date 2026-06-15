import json


def analyze_logs():
    logs = []

    with open("evaluation_logs.json", "r") as f:
        for line in f:
            logs.append(json.loads(line))

    total = len(logs)
    scam_count = sum(1 for l in logs if l["prediction"] == "SCAM")

    avg_confidence = sum(l["final_score"] for l in logs) / total

    print("TOTAL SAMPLES:", total)
    print("SCAM DETECTED:", scam_count)
    print("AVG CONFIDENCE:", avg_confidence)


if __name__ == "__main__":
    analyze_logs()