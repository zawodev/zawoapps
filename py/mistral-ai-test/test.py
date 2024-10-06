from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_PATH = "./local_model"
TOKENIZER_PATH = "./local_tokenizer"

# załadowanie modelu i tokenizera
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH)
# model = AutoModelForCausalLM.from_pretrained(MODEL_PATH) # GPU
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, device_map='cpu') # CPU

# funkcja do generowania odpowiedzi
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors='pt')
    outputs = model.generate(inputs['input_ids'], max_length=50, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Model loaded. You can start typing your prompts.")

# nieskończona pętla do testowania modelu
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        print("Exiting...")
        break
    response = generate_response(user_input)
    print(f"Bot: {response}")
