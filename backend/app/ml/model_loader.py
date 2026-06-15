import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

#singelton storage
_model = None
_tokenizer = None

MODEL_PATH = "models/distilbert_scam_detector"

#load tokenizer
def get_tokenizer():
    global _tokenizer

    if _tokenizer is None:
        _tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)

    return _tokenizer


#load model
def get_model():
    global _model

    if _model is None:
        _model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()

        # Move to best available device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        _model.to(device)

    return _model


#device helper
def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


# prediction function
def predict(text: str):
    """
    Runs inference on a single text input.
    Returns: label + confidence
    """

    tokenizer = get_tokenizer()
    model = get_model()
    device = get_device()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    probs = torch.softmax(logits, dim=1)
    confidence, prediction = torch.max(probs, dim=1)

    label = int(prediction.item())
    confidence = float(confidence.item())

    return {
        "label": label,          # 0 = genuine, 1 = scam
        "confidence": confidence
    }



def load_model():
    """
    Backward compatibility for old code.
    """
    return get_model()