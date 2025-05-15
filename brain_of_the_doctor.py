#Step1: Setup GROQ API key
import os
import base64
from groq import Groq

# Direct API key implementation
GROQ_API_KEY = "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"

#Step2: Convert image to required format
def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM 
def analyze_image_with_query(query, encoded_image, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    client = Groq(api_key=GROQ_API_KEY)
    
    # Create properly formatted message
    message_content = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": str(query)  # Ensure it's a string
            }
        ]
    }
    
    # Add image if provided
    if encoded_image:
        message_content["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"
            }
        })
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[message_content],
            model=model,
            max_tokens=1024
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing image: {str(e)}"
