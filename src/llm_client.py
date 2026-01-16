import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Role Configuration
MODEL_ROLES = {
    "root": "gpt-4o",      # The Manager
    "sub": "gpt-4o-mini"   # The Worker
}

def get_llm_response(messages, role="root"):
    """Fetches response from OpenAI based on the assigned role."""
    try:
        response = client.chat.completions.create(
            model=MODEL_ROLES[role],
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with {role} model: {str(e)}"