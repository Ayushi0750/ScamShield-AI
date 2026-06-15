import os
import pandas as pd
import torch
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

from sklearn.utils.class_weight import compute_class_weight
from torch.nn import CrossEntropyLoss

from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    TrainingArguments,
    Trainer
)

from datasets import Dataset


#mode control
RUN_MODE = "train"   #  CHANGE TO "eval" IF YOU ONLY WANT TESTING

#load datsset
df = pd.read_csv("data/processed/final_data.csv")
df = df.sample(n=6000, random_state=42)


#class imbalance fix
classes = np.array([0, 1])

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=df["label"]
)

class_weights = torch.tensor(class_weights, dtype=torch.float)

print("\nCLASS WEIGHTS:", class_weights)



train_df, val_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,
    stratify=df["label"]
)



train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)



train_dataset = train_dataset.rename_column("label", "labels")
val_dataset = val_dataset.rename_column("label", "labels")



tokenizer = DistilBertTokenizer.from_pretrained(
    "distilbert-base-uncased"
)



def tokenize_function(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )


train_dataset = train_dataset.map(tokenize_function, batched=True)
val_dataset = val_dataset.map(tokenize_function, batched=True)

train_dataset = train_dataset.remove_columns(["text", "__index_level_0__"])
val_dataset = val_dataset.remove_columns(["text", "__index_level_0__"])

train_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

val_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

print("\nTOKENIZATION COMPLETE")



model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

print("\nMODEL LOADED SUCCESSFULLY")
print("NUMBER OF LABELS:", model.config.num_labels)



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print("\nDEVICE:", device)



def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="binary",
        zero_division=0
    )

    accuracy = accuracy_score(labels, predictions)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }



training_args = TrainingArguments(
    output_dir="models/distilbert_scam_detector",

    num_train_epochs=1,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,

    learning_rate=2e-5,
    weight_decay=0.01,

    eval_strategy="epoch",
    save_strategy="epoch",

    logging_steps=20,

    load_best_model_at_end=True,
    report_to="none"
)

print("\nTRAINING ARGUMENTS CREATED")



class WeightedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):

        labels = inputs.get("labels")

        outputs = model(**inputs)
        logits = outputs.get("logits")

        loss_fct = CrossEntropyLoss(weight=class_weights.to(model.device))
        loss = loss_fct(logits, labels)

        return (loss, outputs) if return_outputs else loss


trainer = WeightedTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

print("\nTRAINER INITIALIZED SUCCESSFULLY")


if RUN_MODE == "train":
    print("\nSTARTING TRAINING...\n")
    trainer.train()

    print("\nTRAINING COMPLETED")

    print("\nSAVING MODEL...\n")
    trainer.save_model("models/distilbert_scam_detector")
    tokenizer.save_pretrained("models/distilbert_scam_detector")

# always run evaluation
print("\nRUNNING FINAL EVALUATION...\n")

pred_output = trainer.predict(val_dataset)

logits = pred_output.predictions
labels = pred_output.label_ids
preds = np.argmax(logits, axis=-1)

accuracy = accuracy_score(labels, preds)
precision, recall, f1, _ = precision_recall_fscore_support(
    labels,
    preds,
    average="binary",
    zero_division=0
)

cm = confusion_matrix(labels, preds)

print("\n===== FINAL METRICS =====")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)

print("\n===== CONFUSION MATRIX =====")
print(cm)

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(labels, preds))