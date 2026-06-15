import pandas as pd

df = pd.read_csv("data/processed/final_data.csv")

print("UNIQUE LABELS:")
print(df["label"].unique())

print("\nLABEL DATA TYPE:")
print(df["label"].dtype)

print("\nFIRST 10 LABELS:")
print(df["label"].head(10).tolist())