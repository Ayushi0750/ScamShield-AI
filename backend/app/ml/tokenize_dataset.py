import os
import pandas as pd
from transformers import DistilBertTokenizer



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "final_data.csv")


df = pd.read_csv(DATA_PATH)


tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")


input_ids_list = []
attention_masks_list = []
labels = []

for i, row in df.iterrows():
    text = str(row["text"])
    label = row["label"]

    encoded = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    input_ids_list.append(encoded["input_ids"][0])
    attention_masks_list.append(encoded["attention_mask"][0])
    labels.append(label)


print("Sample Input IDs:", input_ids_list[0])
print("Sample Attention Mask:", attention_masks_list[0])
print("Sample Label:", labels[0])

print("\nDataset Tokenization Complete!")