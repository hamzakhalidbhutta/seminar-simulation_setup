# modesl/train.py
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    Trainer, 
    TrainingArguments
)

print("Initializing HAIMM Gateway Training Pipeline...")

# 1. Load the Dataset you just generated
print("Loading dataset...")
df = pd.read_csv("../datasets/haimm_training_data.csv")

# Split into Training (80%) and Testing (20%)
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert Pandas DataFrames into Hugging Face Datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# 2. Load the Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# 3. Tokenization Function
def tokenize_function(examples):
    # This chops the URIs into sub-word fragments
    return tokenizer(examples["uri"], padding="max_length", truncation=True, max_length=128)

print("Tokenizing data (chopping URLs into mathematical fragments)...")
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_test = test_dataset.map(tokenize_function, batched=True)

# 4. Load the Model (The "Blank Slate")
print("Loading DistilBERT base model...")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# 5. Set up Training Arguments
training_args = TrainingArguments(
    output_dir="./haimm_gateway_model",
    eval_strategy="epoch",       # Check accuracy after every pass
    learning_rate=2e-5,          # Standard learning rate for fine-tuning
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,          # 3 passes over the 10,000 logs is plenty
    weight_decay=0.01,
)

# 6. Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,
)

# 7. TRAIN THE MODEL!
print("\n[!] Starting Neural Training. This may take a few minutes...")
trainer.train()

# 8. Save your Custom "Aviation-Grade" Weights
print("\n[SUCCESS] Training Complete!")
model.save_pretrained("./haimm_gateway_model")
tokenizer.save_pretrained("./haimm_gateway_model")
print("Custom HAIMM Gateway weights saved to './haimm_gateway_model'.")