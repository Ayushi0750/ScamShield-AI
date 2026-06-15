import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# 1. Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# 2. Load DistilBERT model (classification head added)
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2  # 0 = genuine, 1 = scam
)

# 3. Sample text
text = "Congratulations! You are selected. Pay 999 fee to activate your offer."

# 4. Tokenize
inputs = tokenizer(
    text,
    padding=True,
    truncation=True,
    max_length=64,
    return_tensors="pt"
)

# 5. Run model (NO TRAINING YET)
with torch.no_grad():
    outputs = model(**inputs)

# 6. Get logits
logits = outputs.logits

print("Logits:", logits)

# 7. Convert to probabilities
probabilities = torch.softmax(logits, dim=1)

print("Probabilities:", probabilities)

# 8. Final prediction
prediction = torch.argmax(probabilities, dim=1).item()

print("Prediction (0 = Genuine, 1 = Scam):", prediction)