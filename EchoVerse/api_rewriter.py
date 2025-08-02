import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

@st.cache_resource
def load_model():
    model_id = "gpt2"  # Much smaller and faster model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    # Add padding token if it doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return tokenizer, model

def rewrite_text(text):
    tokenizer, model = load_model()
    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)