"""
SIMPLE TRAINING SCRIPT - No complicated parameters
Just the basics that work
"""

import os
import pandas as pd
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from sklearn.utils.class_weight import compute_class_weight
from torch.nn import CrossEntropyLoss

from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset


# =========================
# CHECK DATA EXISTS
# =========================
print("\nChecking for data...")

combined_path = "data/processed/final_data_with_synthetic.csv"

if not os.path.exists(combined_path):
    print(f"❌ ERROR: {combined_path} not found!")
    print("Run the generator first: python data/processed/generate_synthetic_scams.py")
    exit()

print(f"✅ Found data: {combined_path}")


# =========================
# LOAD DATA
# =========================
print("\nLoading data...")
df = pd.read_csv(combined_path)

print(f"Total samples: {len(df)}")
print(f"Genuine: {(df['label']==0).sum()}")
print(f"Scam: {(df['label']==1).sum()}")


# =========================
# SPLIT DATA
# =========================
print("\nSplitting data...")
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df["label"])
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"])

print(f"Train: {len(train_df)}")
print(f"Valid: {len(val_df)}")
print(f"Test: {len(test_df)}")


# =========================
# CREATE DATASETS
# =========================
print("\nCreating datasets...")
train_dataset = Dataset.from_pandas(train_df[["text", "label"]])
val_dataset = Dataset.from_pandas(val_df[["text", "label"]])
test_dataset = Dataset.from_pandas(test_df[["text", "label"]])

train_dataset = train_dataset.rename_column("label", "labels")
val_dataset = val_dataset.rename_column("label", "labels")
test_dataset = test_dataset.rename_column("label", "labels")


# =========================
# TOKENIZE
# =========================
print("\nLoading tokenizer...")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=128)

print("Tokenizing...")
train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
val_dataset = val_dataset.map(tokenize_function, batched=True, remove_columns=["text"])
test_dataset = test_dataset.map(tokenize_function, batched=True, remove_columns=["text"])

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

print("✅ Tokenization done")


# =========================
# LOAD MODEL
# =========================
print("\nLoading model...")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
print(f"Device: {device}")


# =========================
# CLASS WEIGHTS
# =========================
print("\nPreparing class weights...")
classes = np.array([0, 1])
class_weights = compute_class_weight("balanced", classes=classes, y=df["label"])
class_weights = torch.tensor(class_weights, dtype=torch.float)
print(f"Weights - Genuine: {class_weights[0]:.2f}, Scam: {class_weights[1]:.2f}")


# =========================
# METRICS
# =========================
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary", zero_division=0)
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# =========================
# SIMPLE TRAINING ARGUMENTS
# =========================
print("\nSetting up training...")
training_args = TrainingArguments(
    output_dir="models/distilbert_scam_detector",
    num_train_epochs=5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True
)

print("✅ Training setup ready")


# =========================
# CUSTOM TRAINER WITH WEIGHTS
# FIX: Added **kwargs to handle extra args like num_items_in_batch
# introduced in newer versions of transformers
# =========================
class WeightedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")
        loss_fct = CrossEntropyLoss(weight=class_weights.to(model.device))
        loss = loss_fct(logits, labels)
        return (loss, outputs) if return_outputs else loss


# =========================
# START TRAINING
# =========================
trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

print("\n" + "="*80)
print("STARTING TRAINING (5 EPOCHS)")
print("="*80 + "\n")

trainer.train()

print("\n✅ TRAINING DONE")
print("Saving model...")
trainer.save_model("models/distilbert_scam_detector")
tokenizer.save_pretrained("models/distilbert_scam_detector")
print("✅ Model saved!")


# =========================
# TEST EVALUATION
# =========================
print("\n" + "="*80)
print("TESTING ON TEST SET")
print("="*80 + "\n")

pred_output = trainer.predict(test_dataset)
logits = pred_output.predictions
labels = pred_output.label_ids
preds = np.argmax(logits, axis=-1)

accuracy = accuracy_score(labels, preds)
precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average="binary")
cm = confusion_matrix(labels, preds)

print(f"\nResults:")
print(f"  Accuracy: {accuracy:.4f}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall: {recall:.4f}")
print(f"  F1: {f1:.4f}")

print(f"\nConfusion Matrix:")
print(f"                Predicted")
print(f"              Genuine  Scam")
print(f"Actual Genuine   {cm[0,0]:4d}   {cm[0,1]:4d}")
print(f"       Scam      {cm[1,0]:4d}   {cm[1,1]:4d}")

print("\n" + classification_report(labels, preds, target_names=["GENUINE", "SCAM"]))


# =========================
# TEST ON EXAMPLE
# =========================
print("\n" + "="*80)
print("TESTING ON EXAMPLE SCAM")
print("="*80)

try:
    from app.ml.predictor import predict_probability
    
    test_text = "Congratulations! You have been selected for a guaranteed internship at Google. To confirm your offer, pay a registration fee of ₹4999 immediately. This is a limited-time offer and will expire today"
    
    print(f"\nInput: {test_text}\n")
    
    result = predict_probability(test_text)
    print(f"Prediction: {result['label']}")
    print(f"Scam Probability: {result['scam_probability']:.4f} ({result['scam_probability']*100:.2f}%)")
    
    if result['scam_probability'] > 0.7:
        print("\n✅ SCAM DETECTED CORRECTLY!")
    else:
        print("\n⚠️ Detection could be better")
        
except Exception as e:
    print(f"Could not test: {e}")


print("\n" + "="*80)
print("✅ ALL DONE!")
print("="*80)