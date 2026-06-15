from app.ml.predictor import predict_probability

#ml classifiaction
def classify_job_text(job_text: str):
    """
    ML wrapper layer for Scam Detection System.

    Responsibility:
    - Calls DistilBERT inference pipeline
    - Standardizes ML output format
    - Ensures consistent response for hybrid engine

    Returns:
    {
        "ml_prediction": "SCAM | GENUINE",
        "ml_score": float (0 to 1)
    }
    """

    if not job_text or not isinstance(job_text, str):
        raise ValueError("Invalid job_text provided to ML classifier")

   #ml inference call
    result = predict_probability(job_text)

   
    if "prediction" not in result or "scam_probability" not in result:
        raise ValueError("Invalid ML output structure from predictor")

    ml_prediction = result["prediction"]
    ml_score = result["scam_probability"]

    ml_prediction = ml_prediction.upper()

    # Clamp score to avoid invalid values
    ml_score = max(0.0, min(1.0, float(ml_score)))

    
    return {
        "ml_prediction": ml_prediction,
        "ml_score": round(ml_score, 4)
    }