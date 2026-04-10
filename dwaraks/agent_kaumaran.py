
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "sarvamai/sarvam-2b-v0.5"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

# Example: Starting a Tamil spiritual verse
input_text = "திருத்தணியில் உதித்(து) அருளும் ஒருத்தன்மலை விருத்தன்என(து) உளத்தில்உறை கருத்தன்மயில் நடத்துகுகன் வேலே"
inputs = tokenizer(input_text, return_tensors="pt").to("mps")
outputs = model.generate(**inputs, max_new_tokens=50)

print(tokenizer.decode(outputs[0]))