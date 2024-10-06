import os
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset

import wandb
# wandb.login(key="eab2eeb534b4c414640bf5683637114e147036d3")
# os.environ["WANDB_DISABLED"] = "false"

# MODEL_NAME = "openlm-research/open_llama_7b"  # dostosuj do Mistral 7B jeśli jest dostępny

MODEL_PATH = "./local_model"
TOKENIZER_PATH = "./local_tokenizer"
DATA_FILE = 'data.json'
TRAINING_TIME_LIMIT = 1 * 60  # czas treningu w sekundach (np. 1 godzina)

# funkcja do sprawdzenia czy model jest już pobrany
def is_model_downloaded():
    return os.path.exists(MODEL_PATH) and os.path.exists(TOKENIZER_PATH)

if not is_model_downloaded():
    print("Model and tokenizer not found. Please download them manually and place them in the local_model directory.")
else:
    print("Model and tokenizer found. Proceeding with training.")

# załadowanie modelu i tokenizera
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH) # GPU

print(torch.cuda.is_available())  # powinno zwrócić True jesli jest dostępna karta graficzna

# model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, device_map='cpu') # CPU

# dodanie tokena do paddingu, jeśli nie istnieje
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# wczytanie danych
dataset = load_dataset('json', data_files=DATA_FILE)
print(dataset)

# przygotowanie danych do treningu
def preprocess_function(examples):
    inputs = examples['input']  # bez iteracji, używamy bezpośrednio kolumny 'input'
    targets = examples['output']  # używamy bezpośrednio kolumny 'output'

    # tokenizacja wejścia
    model_inputs = tokenizer(inputs, max_length=64, truncation=True, padding='max_length')

    # tokenizacja etykiet (targetów)
    labels = tokenizer(targets, max_length=64, truncation=True, padding='max_length').input_ids

    # przypisanie etykiet do model_inputs
    model_inputs["labels"] = labels
    return model_inputs


tokenized_dataset = dataset.map(preprocess_function, batched=True)

# ustawienia treningowe
training_args = TrainingArguments(
    output_dir='./results',
    report_to='wandb', # 'wandb' 'none'
    num_train_epochs=1,  # ustalony czas treningu
    per_device_train_batch_size=4,
    save_steps=10,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=10,
    max_steps=TRAINING_TIME_LIMIT // (tokenized_dataset['train'].num_rows // 4)  # liczba kroków na podstawie czasu treningu
)

# przeprowadzenie treningu
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
)

print("Starting training...")
start_time = time.time()
trainer.train()
elapsed_time = time.time() - start_time
print(f"Training completed in {elapsed_time:.2f} seconds.")

# zapisanie wytrenowanego modelu
model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(TOKENIZER_PATH)
print("Trained model saved.")
