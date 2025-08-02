from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "ibm-granite/granite-3.1-3b-a800m-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

def rewrite_text(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
