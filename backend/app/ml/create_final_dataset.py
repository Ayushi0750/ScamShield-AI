import pandas as pd
import os
import re
from pathlib import Path

#base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

print(f"Base directory: {BASE_DIR}")
print(f"Raw data directory: {RAW_DATA_DIR}\n")


def parse_csv_with_regex(filepath):
    """Parse malformed CSVs with multi-line quoted fields"""
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        pattern = r'"(.*?)",([01])\s*(?:$|\n(?="))'
        matches = re.findall(pattern, content, re.DOTALL)
        
        rows = []
        for job_text, label in matches:
            clean_text = job_text.strip()
            if len(clean_text) > 50:
                rows.append({
                    'job_text': clean_text,
                    'label': int(label)
                })
        
        return pd.DataFrame(rows) if rows else None
    except Exception as e:
        print(f"   Error parsing {os.path.basename(filepath)}: {e}")
        return None


print("="*60)
print("LOADING DATASETS")
print("="*60)

datasets = []

# BATCH 1
print("\n[1] Batch 1...")
batch1_path = os.path.join(RAW_DATA_DIR, "fake_internship_scam_detection_batch1_FIXED.csv")
df1 = parse_csv_with_regex(batch1_path)
if df1 is not None and len(df1) > 0:
    df1 = df1.rename(columns={'job_text': 'text'})
    datasets.append(('Batch 1', df1))
    print(f"   Loaded: {len(df1)} rows")
else:
    print(f"    Not found or empty: {batch1_path}")
    df1 = pd.DataFrame(columns=['text', 'label'])

# BATCH 2
print("\n[2] Batch 2...")
batch2_path = os.path.join(RAW_DATA_DIR, "fake_internship_scam_detection_batch2_FIXED.csv")
df2 = parse_csv_with_regex(batch2_path)
if df2 is not None and len(df2) > 0:
    df2 = df2.rename(columns={'job_text': 'text'})
    datasets.append(('Batch 2', df2))
    print(f"   Loaded: {len(df2)} rows")
else:
    print(f"   Not found or empty: {batch2_path}")
    df2 = pd.DataFrame(columns=['text', 'label'])

# KAGGLE
print("\n[3] Kaggle fake_job_postings.csv...")
kaggle_path = os.path.join(RAW_DATA_DIR, "fake_job_postings.csv")
if os.path.exists(kaggle_path):
    try:
        df3 = pd.read_csv(kaggle_path, encoding='latin-1')
        print(f"  Loaded: {len(df3)} rows")
        
        # Clean Kaggle dataset
        df3.columns = [c.lower() for c in df3.columns]
        
        # Combine text columns SAFELY
        text_cols = ["title", "company_profile", "description", "requirements", "benefits"]
        text_parts = []
        for col in text_cols:
            if col in df3.columns:
                text_parts.append(df3[col].fillna("").astype(str))
        
        if text_parts:
            df3["text"] = pd.concat(text_parts, axis=1).agg(" ".join, axis=1)
        else:
            df3["text"] = ""
        
        df3["label"] = df3["fraudulent"].astype(int)
        df3 = df3[["text", "label"]]
        
        datasets.append(('Kaggle', df3))
    except Exception as e:
        print(f"   Error loading Kaggle: {e}")
        df3 = pd.DataFrame(columns=['text', 'label'])
else:
    print(f"    Not found: {kaggle_path}")
    df3 = pd.DataFrame(columns=['text', 'label'])

#merge datasets 
print("\n" + "="*60)
print("MERGING DATASETS")
print("="*60)

if not datasets:
    print(" No datasets found! Check your data/raw/ directory.")
    print(f"\nExpected files:")
    print(f"  - {batch1_path}")
    print(f"  - {batch2_path}")
    print(f"  - {kaggle_path}")
    exit(1)


for name, df in datasets:
    if 'text' not in df.columns:
        df['text'] = ""
    if 'label' not in df.columns:
        df['label'] = 0
    df = df[['text', 'label']].copy()

# Concatenate
all_dfs = [df for _, df in datasets]
final_df = pd.concat(all_dfs, ignore_index=True)

print(f"\nDataset Breakdown:")
for name, df in datasets:
    print(f"  • {name}: {len(df):,} rows")
print(f"  {'─'*40}")
print(f"  TOTAL: {len(final_df):,} rows")

# Label distribution
print(f"\nLabel Distribution (Before Cleaning):")
label_counts = final_df['label'].value_counts().sort_index()
for label, count in label_counts.items():
    pct = count / len(final_df) * 100
    status = "Legitimate (0)" if label == 0 else "Scams (1)"
    print(f"  {status}: {count:,} ({pct:.1f}%)")


# clean data
print(f"\n" + "="*60)
print("CLEANING DATA")
print("="*60)

initial_count = len(final_df)

# Remove nulls
final_df = final_df.dropna(subset=['text', 'label'])

# Remove very short text
final_df = final_df[final_df['text'].str.len() > 50]

# Remove duplicates
final_df = final_df.drop_duplicates(subset=['text'], keep='first')

# Convert label to int
final_df['label'] = final_df['label'].astype(int)

removed = initial_count - len(final_df)
print(f"Removed {removed:,} invalid rows")
print(f"Final dataset: {len(final_df):,} rows")

# Label distribution after cleaning
print(f"\nLabel Distribution (After Cleaning):")
label_counts = final_df['label'].value_counts().sort_index()
for label, count in label_counts.items():
    pct = count / len(final_df) * 100
    status = "Legitimate (0)" if label == 0 else "Scams (1)"
    print(f"  {status}: {count:,} ({pct:.1f}%)")

# Shuffle
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)
#o/p
print(f"\n" + "="*60)
print("SAVING DATASET")
print("="*60)

output_path = os.path.join(PROCESSED_DATA_DIR, "final_data.csv")
final_df.to_csv(output_path, index=False)

print(f"\n Dataset saved successfully!")
print(f"   Path: {output_path}")
print(f"   Size: {len(final_df):,} rows × {len(final_df.columns)} columns")

print(f"\n" + "="*60)
print("SAMPLE DATA (First 3 rows)")
print("="*60)
print(final_df.head(3).to_string())
print(f"\n Done!")