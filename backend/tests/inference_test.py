import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

# Test texts
test_texts = [
    "Software Engineer Intern at TCS. Interview required. Apply through official portal.",
    "Congratulations! You are selected. Pay 999 fee to activate your offer letter.",
    "Data Analyst role. SQL knowledge required. Multiple interview rounds.",
    "Earn 5000 per day from home. No experience needed. Limited seats available."
]

for text in test_texts:

    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)

    prediction = torch.argmax(probabilities, dim=1).item()

    print("\n" + "=" * 60)
    print("TEXT:")
    print(text)

    print("\nLOGITS:")
    print(logits)

    print("\nPROBABILITIES:")
    print(probabilities)

    print("\nPREDICTION:")
    print("Genuine" if prediction == 0 else "Scam")