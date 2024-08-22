import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_name = "NexaAIDev/Octopus-v4"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(question):
    inputs = f"<|system|>You are a router. Below is the query from the users, please call the correct function and generate the parameters to call the function.<|end|><|user|>{question}<|end|><|assistant|>"
    input_ids = tokenizer(inputs, return_tensors="pt")['input_ids'].to(model.device)
    generated_token_ids = []

    for _ in range(200):
        next_token = model(input_ids).logits[:, -1].argmax(-1)
        generated_token_ids.append(next_token.item())
        input_ids = torch.cat([input_ids, next_token.unsqueeze(1)], dim=-1)
        if next_token.item() == 32041:  # <nexa_end> token
            break

    return tokenizer.decode(generated_token_ids)

def chatbot():
    print("Chatbot: Hello! I'm the Octopus-v4 router. How can I assist you today? (Type 'exit' to end the conversation)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = generate_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    chatbot()