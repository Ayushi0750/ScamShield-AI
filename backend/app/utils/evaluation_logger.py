import json
from datetime import datetime


def log_evaluation(data: dict):
    """
    Logs every prediction for later analysis
    """

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input_text": data.get("input_text"),
        "rule_score": data.get("rule_score"),
        "ml_score": data.get("ml_score"),
        "rag_score": data.get("rag_score"),
        "final_score": data.get("final_score"),
        "prediction": data.get("prediction"),
        "risk_level": data.get("risk_level"),
        "agreement_status": data.get("agreement_status"),

       
        "actual_label": data.get("actual_label")
    }

    with open("evaluation_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")