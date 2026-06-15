const resultDiv = document.getElementById("result");

document.getElementById("scanBtn").addEventListener("click", async () => {
    resultDiv.innerText = "Analyzing current page...";

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => document.body.innerText
        });

        const pageText = results[0].result;

        const response = await fetch("http://localhost:8000/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_text: pageText,
                actual_label: 0
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        resultDiv.innerText = `
Status: ${data.is_scam ? "🚨 SCAM" : "✅ SAFE"}

Confidence: ${(data.confidence * 100).toFixed(2)}%

Risk Level: ${data.risk_level}

ML Prediction: ${data.ml_prediction}
        `;

    } catch (error) {
        console.error(error);

        resultDiv.innerText =
            "❌ Error: Could not analyze page.\n\nCheck backend connection and console logs.";
    }
});