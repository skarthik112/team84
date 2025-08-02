import requests
import streamlit as st
import time

def rewrite_text(text):
    """
    Uses Hugging Face Inference API for text rewriting.
    No local model needed - runs in the cloud!
    """
    # Using a free model that's good for text rewriting
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    
    # Create a prompt for rewriting
    prompt = f"Rewrite this text to make it more engaging and narrative: {text}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', text)
                return generated_text
            else:
                return text
        elif response.status_code == 503:
            # Model is loading, try again after a short wait
            st.warning("AI model is warming up... trying again in a moment")
            time.sleep(3)
            response = requests.post(API_URL, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', text)
        
        # If API fails, return original text
        st.warning("AI rewriting temporarily unavailable, using original text")
        return text
        
    except Exception as e:
        st.warning(f"AI rewriting error: {str(e)}")
        return text