import pandas as pd
import requests

URL = "http://127.0.0.1:8000/api/analyze"


def get_label(confidence):
    return "SCAM" if confidence >= 0.5 else "GENUINE"


def safe_get(row, keys):
    for k in keys:
        if k in row:
            return row[k]
    return None


def run_test():

    df = pd.read_csv("data/processed/final_data.csv")

    total = 0
    correct = 0

    scam_correct = 0
    scam_total = 0

    genuine_correct = 0
    genuine_total = 0

    llm_agreement = 0

    for i, row in df.iterrows():

        # -------------------
        # SAFE INPUT EXTRACTION
        # -------------------
        job_text = safe_get(row, ["job_text", "text", "description"])
        actual = safe_get(row, ["label", "target", "is_scam"])

        # -------------------
        # VALIDATION
        # -------------------
        if pd.isna(job_text) or job_text is None:
            continue

        job_text = str(job_text).strip()

        if len(job_text) < 10:
            continue

        # 🔥 FIX: truncate long text (API limit 5000 chars)
        if len(job_text) > 5000:
            job_text = job_text[:5000]

        # -------------------
        # LABEL NORMALIZATION
        # -------------------
        if isinstance(actual, str):
            actual = actual.upper().strip()
        else:
            actual = "SCAM" if actual == 1 else "GENUINE"

        payload = {
            "job_text": job_text,
            "actual_label": actual
        }

        try:
            res = requests.post(URL, json=payload)

            # -------------------
            # HANDLE API FAILURES
            # -------------------
            if res.status_code != 200:
                print(f"\nAPI ERROR at row {i}: {res.status_code}")
                print("Response:", res.text)
                continue

            data = res.json()

            # -------------------
            # SAFE CONFIDENCE EXTRACTION
            # -------------------
            confidence = data.get("confidence", None)

            if confidence is None:
                print(f"Missing confidence at row {i}: {data}")
                continue

            pred = get_label(confidence)

            # -------------------
            # METRICS
            # -------------------
            total += 1

            if pred == actual:
                correct += 1

            if actual == "SCAM":
                scam_total += 1
                if pred == "SCAM":
                    scam_correct += 1

            if actual == "GENUINE":
                genuine_total += 1
                if pred == "GENUINE":
                    genuine_correct += 1

            # -------------------
            # LLM ALIGNMENT
            # -------------------
            llm_verdict = data.get("verdict", "UNKNOWN")
            if llm_verdict != "UNKNOWN" and llm_verdict == pred:
                llm_agreement += 1

            # -------------------
            # PROGRESS
            # -------------------
            if total % 50 == 0:
                print(f"Processed {total} valid samples...")

        except Exception as e:
            print(f"Error at row {i}: {e}")

    # -------------------
    # FINAL METRICS
    # -------------------
    accuracy = correct / total if total else 0
    scam_recall = scam_correct / scam_total if scam_total else 0
    genuine_recall = genuine_correct / genuine_total if genuine_total else 0
    llm_alignment = llm_agreement / total if total else 0

    print("\n========================")
    print("FINAL SYSTEM EVALUATION")
    print("========================")

    print(f"Total Valid Samples: {total}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"SCAM Recall: {scam_recall:.4f}")
    print(f"Genuine Recall: {genuine_recall:.4f}")
    print(f"LLM Alignment: {llm_alignment:.4f}")


if __name__ == "__main__":
    run_test()