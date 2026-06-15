import React, { useState } from "react";
import axios from "axios";
import ResultCard from "./ResultCard";
import "../App.css";

const Analyzer = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text) return;

    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/analyze",
        {
          job_text: text,
          actual_label: 0,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setResult({
        error: "Backend not working or request format issue",
      });
    }

    setLoading(false);
  };

  return (
    <div className="page-container">

      <div className="hero-section">
        <h1>🛡 Scam Shield AI</h1>

        <p>
          AI-Powered Internship & Job Scam Detection Platform
        </p>
      </div>

      <div className="analyzer-card">

        <h2>Analyze Job / Internship Posting</h2>

        <textarea
          className="job-textarea"
          placeholder="Paste the complete job or internship description here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          className="analyze-btn"
          onClick={handleAnalyze}
        >
          {loading ? "Analyzing..." : "Analyze Posting"}
        </button>

        {result && <ResultCard result={result} />}

      </div>

    </div>
  );
};

export default Analyzer