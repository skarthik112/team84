import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    # Using a very small, fast model for text generation
    generator = pipeline(
        'text-generation',
        model='distilgpt2',  # Much smaller than GPT-2
        tokenizer='distilgpt2',
        device=-1  # Use CPU, not GPU
    )
    return generator

def rewrite_text(text):
    generator = load_model()
    
    # Create a prompt for rewriting
    prompt = f"Rewrite this text in an engaging, narrative style:\n\n{text}\n\nRewritten version:"
    
    try:
        # Generate with the model
        result = generator(
            prompt,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=generator.tokenizer.eos_token_id,
            truncation=True
        )
        
        generated_text = result[0]['generated_text']
        
        # Extract only the rewritten part (after "Rewritten version:")
        if "Rewritten version:" in generated_text:
            rewritten = generated_text.split("Rewritten version:")[-1].strip()
            return rewritten if rewritten else text
        else:
            # If no clear separation, return the generated text minus the original prompt
            return generated_text[len(prompt):].strip() or text
            
    except Exception as e:
        st.error(f"AI rewriting error: {str(e)}")
        return text
