from transformers import DistilBertTokenizer

# 1. Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# 2. Sample scam text
text = "Work from home job. Earn 5000 per day. Pay 999 registration fee to start immediately."

# 3. Tokenize text
encoded = tokenizer(
    text,
    padding="max_length",
    truncation=True,
    max_length=64,
    return_tensors="pt"
)

# 4. Print outputs
print("\n=== INPUT IDS ===")
print(encoded["input_ids"])

print("\n=== ATTENTION MASK ===")
print(encoded["attention_mask"])

# 5. Decode tokens (for understanding)
print("\n=== TOKENS ===")
print(tokenizer.convert_ids_to_tokens(encoded["input_ids"][0]))