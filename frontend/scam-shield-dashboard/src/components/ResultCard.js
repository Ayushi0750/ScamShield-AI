import React from "react";

const ResultCard = ({ result }) => {

  if (result.error) {
    return (
      <div className="error-card">
        {result.error}
      </div>
    );
  }

  

  const mlPrediction =
    result.ml_prediction ||
    (result.ml_score >= 70 ? "SCAM" : "GENUINE");

  const rulePrediction =
    result.rule_prediction ||
    (result.master_risk?.breakdown?.rule_score >= 60
      ? "SCAM"
      : "GENUINE");

  const agreementStatus =
    mlPrediction === rulePrediction ? "AGREE" : "CONFLICT";

  return (
    <div className="result-card">

      <h3>Analysis Result</h3>

      <div className="status-box">

        <h2>
          {result.is_scam
            ? "🚨 SCAM DETECTED"
            : "✅ SAFE POSTING"}
        </h2>

        <p>
          Confidence: {(result.confidence * 100).toFixed(2)}%
        </p>

        <p>
          Risk Level: {result.risk_level}
        </p>

      </div>

      <hr />

      <h4>Model Predictions</h4>

      <p>
        <strong>Rule Prediction:</strong>{" "}
        {rulePrediction}
      </p>

      <p>
        <strong>ML Prediction:</strong>{" "}
        {mlPrediction}
      </p>

      <p>
        <strong>ML Score:</strong>{" "}
        {(result.ml_score * 100).toFixed(2)}%
      </p>

      <p>
        <strong>Agreement Status:</strong>{" "}
        {agreementStatus}
      </p>

      <hr />

      {/* RAG SECTION */}

      <h4>RAG (Similar Cases Found)</h4>

      {result.rag && result.rag.top_matches?.length > 0 ? (
        <>
          <p>
            <strong>RAG Score:</strong>{" "}
            {(result.rag.score * 100).toFixed(2)}%
          </p>

          <ul>
            {result.rag.top_matches.map((item, idx) => (
              <li key={idx}>
                <strong>{item.label}</strong> —{" "}
                {item.text?.slice(0, 120)}...
                <br />
                <small>
                  Similarity: {(item.similarity * 100).toFixed(2)}%
                </small>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p>No similar cases found.</p>
      )}

      <hr />

      <h4>Matched Scam Indicators</h4>

      {result.matched_rules?.length > 0 ? (
        <ul>
          {result.matched_rules.map((rule, idx) => (
            <li key={idx}>
              <strong>{rule.rule_name}</strong> — {rule.reason}
            </li>
          ))}
        </ul>
      ) : (
        <p>No suspicious indicators found.</p>
      )}

      <hr />

      <h4>Master Risk Analysis</h4>

      <pre>
        {JSON.stringify(result.master_risk, null, 2)}
      </pre>

    </div>
  );
};

export default ResultCard;