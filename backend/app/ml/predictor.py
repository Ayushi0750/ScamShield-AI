import torch
from app.ml.preprocess import preprocess_text
from app.ml.model_loader import get_model, get_tokenizer



tokenizer = get_tokenizer()
model = get_model()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


#tokenize
def tokenize_text(text):
    return tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="pt"
    )



def run_model(inputs):
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.logits


#probability conversion
def get_probabilities(logits):
    probs = torch.softmax(logits, dim=1)

    return {
        "genuine_probability": float(probs[0][0]),
        "scam_probability": float(probs[0][1])
    }


# pipeline
def predict_probability(text):

    cleaned_text = preprocess_text(text)

    inputs = tokenize_text(cleaned_text)

    logits = run_model(inputs)

    probabilities = get_probabilities(logits)

    scam_prob = probabilities["scam_probability"]
    genuine_prob = probabilities["genuine_probability"]

    return {
        "label": "SCAM" if scam_prob > genuine_prob else "GENUINE",
        "confidence": max(scam_prob, genuine_prob),
        "scam_probability": scam_prob,
        "genuine_probability": genuine_prob
    }